#!/usr/bin/env python3
"""
One-time backfill script: generates notes for all articles in seen_*.json
that don't already have a corresponding note in notes/.

Safe to run multiple times — skips any article that already has a note.
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic
import feedparser
import httpx
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
NOTES_DIR = SCRIPT_DIR / "notes"
ENV_PATH = SCRIPT_DIR / ".env"

if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            k, v = key.strip(), value.strip()
            if not os.environ.get(k):
                os.environ[k] = v

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_seen(seen_file: str) -> list[str]:
    path = SCRIPT_DIR / seen_file
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def get_existing_note_urls() -> set[str]:
    """Scan all notes in notes/ and extract their source URLs."""
    urls = set()
    if not NOTES_DIR.exists():
        return urls
    for md_file in NOTES_DIR.rglob("*.md"):
        if md_file.parent.name == "Digests":
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            m = re.search(r"\*\*Source\*\*: \[.+?\]\((.+?)\)", text)
            if m:
                urls.add(m.group(1))
        except Exception:
            continue
    return urls


def get_existing_note_titles() -> list[str]:
    """Scan existing notes for cross-linking."""
    notes = []
    if NOTES_DIR.exists():
        for md_file in NOTES_DIR.rglob("*.md"):
            if md_file.parent.name != "Digests":
                notes.append(md_file.stem)
    return notes


def fetch_article_metadata(feed_url: str) -> dict[str, dict]:
    """Fetch RSS feed and return a map of URL -> article metadata."""
    feed = feedparser.parse(feed_url)
    articles = {}
    for entry in feed.entries:
        url = entry.get("link", "")
        if not url:
            continue
        published = ""
        published_iso = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            published = dt.strftime("%b %d, %Y")
            published_iso = dt.strftime("%Y-%m-%d")
        articles[url] = {
            "title": entry.get("title", "Untitled"),
            "url": url,
            "published": published,
            "published_iso": published_iso,
            "description": entry.get("summary", ""),
        }
    return articles


def fetch_article_content(url: str) -> str:
    """Fetch full article page and extract text content."""
    try:
        resp = httpx.get(url, follow_redirects=True, timeout=30)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        log.warning(f"Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.select_one(".body.markup") or soup.select_one("article") or soup.select_one(".post-content")
    if content_div:
        for tag in content_div.find_all(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = content_div.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    if len(text) > 8000:
        text = text[:8000] + "\n[... truncated]"
    return text


def sanitize_filename(title: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > 80:
        cleaned = cleaned[:80].rsplit(" ", 1)[0]
    return cleaned


def generate_summary(
    client: anthropic.Anthropic,
    model: str,
    feed_name: str,
    feed_author: str,
    title: str,
    content: str,
    published: str,
    existing_notes: list[str],
) -> dict:
    existing_list = "\n".join(f"- {n}" for n in existing_notes) if existing_notes else "None yet"

    prompt = f"""Analyze this article and return a JSON object with these fields:

1. "summary": A 1-2 sentence summary of the article's core argument.

2. "takeaways": An array of 3-5 key takeaway strings. Each should be actionable and specific. Start each with a bolded phrase.

3. "author": The default author of this feed is {feed_author}. Use this unless the article features a guest, in which case use "{feed_author} (featuring Guest Name)".

4. "related": An array of 2-3 filenames from the existing notes list below that are most related to this article. Use exact filenames.

This article is from: {feed_name}

Existing notes in the vault:
{existing_list}

Article title: {title}
Published: {published}

Article content:
{content}

Return ONLY valid JSON, no markdown fences or other text."""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def format_note(title: str, url: str, published: str, feed_name: str, result: dict) -> str:
    lines = [
        f"# {title}",
        "",
        f"**Source**: [{feed_name}]({url})",
        f"**Author**: {result.get('author', 'Unknown')} | **Date**: {published}",
        "",
        "---",
        "",
        "## Summary",
        "",
        result.get("summary", ""),
        "",
        "## Key Takeaways",
        "",
    ]
    for takeaway in result.get("takeaways", []):
        lines.append(f"- {takeaway}")
    lines.extend(["", "## Related", ""])
    for related in result.get("related", []):
        lines.append(f"- [[{related}]]")
    return "\n".join(lines) + "\n"


def main():
    config = load_config()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(max_retries=5)
    feeds = config.get("feeds", [])

    # Find all URLs that already have notes
    existing_urls = get_existing_note_urls()
    existing_notes = get_existing_note_titles()
    log.info(f"Found {len(existing_urls)} existing notes in notes/")

    total_missing = 0
    total_processed = 0
    total_skipped = 0

    for feed_config in feeds:
        feed_name = feed_config["name"]
        feed_author = feed_config.get("author", "Unknown")
        seen_file = feed_config["seen_file"]

        # Get all URLs we've previously seen
        seen_urls = load_seen(seen_file)
        if not seen_urls:
            log.info(f"No seen URLs for {feed_name}, skipping")
            continue

        # Find which seen URLs are missing notes
        missing_urls = [url for url in seen_urls if url not in existing_urls]
        if not missing_urls:
            log.info(f"{feed_name}: all {len(seen_urls)} articles have notes")
            continue

        log.info(f"{feed_name}: {len(missing_urls)} of {len(seen_urls)} articles need notes")
        total_missing += len(missing_urls)

        # Fetch RSS to get metadata (title, date) for the missing URLs
        try:
            rss_articles = fetch_article_metadata(feed_config["url"])
        except Exception as e:
            log.warning(f"Failed to fetch RSS for {feed_name}: {e}")
            rss_articles = {}

        for url in missing_urls:
            # Try to get metadata from RSS
            article = rss_articles.get(url)
            if not article:
                # Article is no longer in the RSS feed — fetch page directly
                log.info(f"Not in RSS, fetching directly: {url}")
                content = fetch_article_content(url)
                if not content:
                    log.warning(f"Could not fetch {url}, skipping")
                    total_skipped += 1
                    continue
                # Extract title from content
                soup = BeautifulSoup(content, "html.parser")
                title = soup.title.string if soup.title else "Untitled"
                article = {
                    "title": title,
                    "url": url,
                    "published": "",
                    "published_iso": "",
                    "description": "",
                }
            else:
                content = fetch_article_content(url)
                if not content:
                    content = BeautifulSoup(article["description"], "html.parser").get_text()

            try:
                result = generate_summary(
                    client=client,
                    model=config["model"],
                    feed_name=feed_name,
                    feed_author=feed_author,
                    title=article["title"],
                    content=content,
                    published=article["published"],
                    existing_notes=existing_notes,
                )

                feed_dir = NOTES_DIR / feed_name
                feed_dir.mkdir(parents=True, exist_ok=True)

                date_prefix = article.get("published_iso", "")
                title_part = sanitize_filename(article["title"])
                filename = f"{date_prefix} {title_part}.md" if date_prefix else f"{title_part}.md"
                note_path = feed_dir / filename

                note_content = format_note(
                    title=article["title"],
                    url=url,
                    published=article["published"],
                    feed_name=feed_name,
                    result=result,
                )
                note_path.write_text(note_content, encoding="utf-8")
                log.info(f"Wrote: {note_path.relative_to(SCRIPT_DIR)}")

                existing_notes.append(sanitize_filename(article["title"]))
                existing_urls.add(url)
                total_processed += 1

            except Exception as e:
                log.error(f"Failed to process '{article['title']}': {e}")
                total_skipped += 1
                continue

            time.sleep(1)

    log.info(f"Backfill complete. {total_processed} notes created, {total_skipped} skipped, {total_missing} were missing.")


if __name__ == "__main__":
    main()
