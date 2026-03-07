#!/usr/bin/env python3
"""
Cloud-based Weekly PM Digest Generator

Fetches RSS feeds, reuses summaries from the daily ingest (notes/ directory),
ranks articles by relevance using Claude, and sends a weekly digest email
via Resend. Only calls Claude for the ranking step and any articles not
already summarized by ingest_cloud.py.

Designed to run in GitHub Actions.
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import anthropic
import feedparser
import httpx
import resend
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
NOTES_DIR = SCRIPT_DIR / "notes"
ENV_PATH = SCRIPT_DIR / ".env"

# Load .env file if it exists (local development only)
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


def fetch_feed(feed_url: str) -> list[dict]:
    """Parse RSS feed and return list of article entries."""
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        published = ""
        published_iso = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            published = dt.strftime("%b %d, %Y")
            published_iso = dt.strftime("%Y-%m-%d")
        articles.append({
            "title": entry.get("title", "Untitled"),
            "url": entry.get("link", ""),
            "published": published,
            "published_iso": published_iso,
            "description": entry.get("summary", ""),
        })
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
    content_div = (
        soup.select_one(".body.markup")
        or soup.select_one("article")
        or soup.select_one(".post-content")
    )
    if content_div:
        for tag in content_div.find_all(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = content_div.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    if len(text) > 8000:
        text = text[:8000] + "\n[... truncated]"
    return text


def collect_recent_articles(feeds: list[dict], days: int = 7) -> list[dict]:
    """Fetch all feeds and return articles published in the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    articles = []

    for feed_config in feeds:
        feed_name = feed_config["name"]
        feed_author = feed_config.get("author", "Unknown")
        log.info(f"Fetching feed: {feed_name}")

        try:
            feed_articles = fetch_feed(feed_config["url"])
        except Exception as e:
            log.warning(f"Failed to fetch feed {feed_name}: {e}")
            continue

        for article in feed_articles:
            if not article["published_iso"]:
                continue
            try:
                article_date = datetime.strptime(article["published_iso"], "%Y-%m-%d")
            except ValueError:
                continue
            if article_date < cutoff:
                continue

            article["feed_name"] = feed_name
            article["feed_author"] = feed_author
            articles.append(article)

    articles.sort(key=lambda a: a.get("published_iso", ""), reverse=True)
    log.info(f"Found {len(articles)} articles from the past {days} days")
    return articles


def generate_summary(
    client: anthropic.Anthropic,
    model: str,
    feed_name: str,
    feed_author: str,
    title: str,
    content: str,
    published: str,
) -> dict:
    """Use Claude to generate a structured summary."""
    prompt = f"""Analyze this article and return a JSON object with these fields:

1. "summary": A 1-2 sentence summary of the article's core argument.

2. "takeaways": An array of 3-5 key takeaway strings. Each should be actionable and specific. Start each with a bolded phrase.

3. "author": The default author of this feed is {feed_author}. Use this unless the article features a guest, in which case use "{feed_author} (featuring Guest Name)".

This article is from: {feed_name}

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


def generate_ranking(
    client: anthropic.Anthropic,
    model: str,
    articles: list[dict],
) -> list[dict]:
    """Rank articles by strategic relevance using Claude."""
    articles_text = ""
    for i, a in enumerate(articles):
        articles_text += (
            f"\n[{i}] \"{a['title']}\" ({a.get('feed_name', 'Unknown')}, "
            f"{a.get('author', 'Unknown')}, {a.get('date', '')})\n"
            f"Summary: {a['summary']}\n"
        )

    prompt = f"""You are helping a VP of Product at a Series C venture-funded B2B SaaS startup prioritize their weekly reading.

Here are {len(articles)} new articles from PM newsletters this week:
{articles_text}

Rank ALL articles by strategic relevance to this leader's priorities:
- Scaling product org & team
- Product-led growth and expansion revenue
- AI/ML product strategy and integration
- Enterprise product management
- Strategic planning and roadmapping

Return a JSON array where each element has:
- "index": the original article index number
- "rank": 1 = most relevant
- "relevance": A single phrase explaining why this matters to a VP of Product
- "must_read": boolean, true only for the top 3 most actionable articles
- "expanded_summary": ONLY for the top 3 must-read articles, provide a 3-4 sentence expanded summary that gives a VP enough context to understand the core argument and why it matters without reading the full article. For non-must-read articles, omit this field.

Sort by rank (1 first). Return ONLY valid JSON, no markdown fences or other text."""

    log.info(f"Ranking {len(articles)} articles...")
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def load_cached_notes(days: int = 7) -> dict[str, dict]:
    """Load article summaries already generated by ingest_cloud.py.

    Returns a dict keyed by article title mapping to parsed note data.
    Only includes notes from the last N days based on filename date prefix.
    """
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cached = {}

    if not NOTES_DIR.exists():
        return cached

    for md_file in NOTES_DIR.rglob("*.md"):
        # Skip digests
        if md_file.parent.name == "Digests":
            continue

        # Filter by date prefix in filename (e.g., "2026-03-05 Title.md")
        name = md_file.stem
        if len(name) >= 10 and name[:4].isdigit():
            file_date = name[:10]
            if file_date < cutoff:
                continue

        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Parse the structured markdown note
        title = ""
        summary = ""
        takeaways = []
        author = ""
        date = ""
        url = ""
        feed_name = md_file.parent.name  # directory name = feed name

        section = None
        for line in text.splitlines():
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            elif line.startswith("**Source**:"):
                # Extract feed name and URL from: **Source**: [Feed](url)
                m = re.search(r"\[(.+?)\]\((.+?)\)", line)
                if m:
                    feed_name = m.group(1)
                    url = m.group(2)
            elif line.startswith("**Author**:"):
                # Extract author and date from: **Author**: Name | **Date**: Date
                m = re.match(r"\*\*Author\*\*: (.+?) \| \*\*Date\*\*: (.+)", line)
                if m:
                    author = m.group(1).strip()
                    date = m.group(2).strip()
            elif line.startswith("## Summary"):
                section = "summary"
            elif line.startswith("## Key Takeaways"):
                section = "takeaways"
            elif line.startswith("## Related"):
                section = None
            elif section == "summary" and line.strip():
                summary = line.strip()
                section = None
            elif section == "takeaways" and line.startswith("- "):
                takeaways.append(line)

        if title and summary:
            cached[title] = {
                "title": title,
                "url": url,
                "feed_name": feed_name,
                "author": author,
                "date": date,
                "summary": summary,
                "takeaways": takeaways,
            }

    log.info(f"Loaded {len(cached)} cached note(s) from notes/")
    return cached


def build_feed_homepage_map(feeds: list[dict]) -> dict[str, str]:
    """Map feed name -> blog homepage URL."""
    result = {}
    for feed in feeds:
        url = re.sub(r"/feed/?$", "", feed["url"])
        url = re.sub(r"/index\.xml$", "", url)
        result[feed["name"]] = url
    return result


def format_digest(
    articles: list[dict],
    ranking: list[dict],
    week_start: str,
    week_end: str,
    feeds: list[dict] | None = None,
) -> str:
    """Format the ranked digest as markdown."""
    feed_counts = {}
    for a in articles:
        name = a.get("feed_name", "Unknown")
        feed_counts[name] = feed_counts.get(name, 0) + 1

    lines = [
        f"# Weekly PM Digest — {week_end}",
        "",
        f"{len(articles)} articles from {len(feed_counts)} feeds | {week_start} – {week_end}",
        "",
    ]

    # Must-reads — expanded treatment
    must_reads = [r for r in ranking if r.get("must_read")]
    if must_reads:
        lines.extend(["---", "", "## Must-Read", ""])
        for r in must_reads:
            a = articles[r["index"]]
            title_link = f"[{a['title']}]({a['url']})" if a.get("url") else a["title"]
            summary = r.get("expanded_summary") or a["summary"]
            entry = [
                f"### {r['rank']}. {title_link}",
                f"*{a.get('feed_name', '')}* — {a.get('author', '')} — {a.get('date', '')}",
                "",
                summary,
                "",
                f"**Why it matters**: {r.get('relevance', '')}",
                "",
            ]
            for t in a.get("takeaways", []):
                entry.append(t)
            entry.extend([
                "",
                f"[Read article →]({a.get('url', '')})",
                "",
                "---",
                "",
            ])
            lines.extend(entry)

    # All other articles
    non_must_reads = [r for r in ranking if not r.get("must_read")]
    if non_must_reads:
        lines.extend(["## All Articles", ""])
        for r in non_must_reads:
            a = articles[r["index"]]
            title_link = f"[{a['title']}]({a['url']})" if a.get("url") else a["title"]
            date = a.get("date", "")
            entry = [
                f"**{r['rank']}.** {title_link} — *{a.get('feed_name', '')}*{' · ' + date if date else ''}",
                "",
                a["summary"],
                "",
            ]
            for t in a.get("takeaways", []):
                entry.append(t)
            entry.append("")
            lines.extend(entry)

    return "\n".join(lines) + "\n"


def _md_links(text: str) -> str:
    """Convert markdown [text](url) links to HTML <a> tags."""
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)


def markdown_to_html(md: str) -> str:
    """Convert digest markdown to simple HTML for email."""
    lines = md.splitlines()
    html_parts = []

    for line in lines:
        stripped = line.strip()

        if stripped == "---":
            html_parts.append('<hr style="border:none;border-top:1px solid #e0e0e0;margin:24px 0;">')
            continue

        if not stripped:
            continue

        if stripped.startswith("### "):
            text = _md_links(stripped[4:])
            html_parts.append(f'<h3 style="margin-bottom:4px;">{text}</h3>')
        elif stripped.startswith("## "):
            html_parts.append(f'<h2 style="margin-top:28px;">{stripped[3:]}</h2>')
        elif stripped.startswith("# "):
            html_parts.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("- "):
            text = stripped[2:]
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            html_parts.append(
                f'<p style="margin-left:20px;margin-top:2px;margin-bottom:2px;color:#444;">'
                f"&bull; {text}</p>"
            )
        elif stripped.startswith("> "):
            html_parts.append(
                f'<blockquote style="border-left:3px solid #ccc;padding-left:12px;'
                f'color:#555;margin:5px 0;">{stripped[2:]}</blockquote>'
            )
        elif re.match(r"^\[Read article", stripped):
            text = _md_links(stripped)
            html_parts.append(f'<p style="margin-top:12px;">{text}</p>')
        elif stripped.startswith("**") and ".**" in stripped and stripped[2:3].isdigit():
            # Article header line: **4.** [Title](url) — *Feed* · Date
            text = _md_links(stripped)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            html_parts.append(f'<p style="margin-top:20px;margin-bottom:4px;">{text}</p>')
        elif stripped.startswith("**") and "**:" in stripped:
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            html_parts.append(f"<p>{text}</p>")
        elif stripped.startswith("*") and not stripped.startswith("**"):
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", stripped)
            html_parts.append(f"<p style='color:#666;margin-top:0;'>{text}</p>")
        else:
            text = _md_links(stripped)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            html_parts.append(f"<p>{text}</p>")

    body = "\n".join(html_parts)
    return (
        '<div style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,'
        'Helvetica,Arial,sans-serif;max-width:700px;margin:0 auto;padding:20px;'
        f'color:#333;">{body}</div>'
    )


def send_digest_email(config: dict, digest_content: str, week_end: str) -> None:
    """Send the digest via Resend API."""
    email_config = config.get("digest_email", {})
    if not email_config.get("enabled"):
        log.info("Email delivery disabled in config")
        return

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        log.warning("RESEND_API_KEY not set — skipping email delivery")
        return

    resend.api_key = api_key
    html = markdown_to_html(digest_content)

    params = {
        "from": email_config["from"],
        "to": email_config["to"],
        "subject": f"Weekly PM Digest - {week_end}",
        "html": html,
    }

    try:
        result = resend.Emails.send(params)
        log.info(f"Digest email sent: {result.get('id', 'OK')}")
    except Exception as e:
        log.error(f"Failed to send digest email: {e}")


def main():
    config = load_config()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(max_retries=5)
    feeds = config.get("feeds", [])

    # Fetch recent articles from all feeds
    articles = collect_recent_articles(feeds, days=7)
    if not articles:
        log.info("No articles from the past 7 days. Skipping digest.")
        return

    # Load summaries already generated by the daily ingest
    cached_notes = load_cached_notes(days=7)

    # Populate articles from cache or fall back to Claude API
    cache_hits = 0
    api_calls = 0
    for i, article in enumerate(articles):
        cached = cached_notes.get(article["title"])
        if cached:
            article["summary"] = cached["summary"]
            article["takeaways"] = cached["takeaways"]
            article["author"] = cached["author"]
            article["date"] = cached["date"] or article["published"]
            cache_hits += 1
            log.info(f"Cache hit: {article['title']}")
            continue

        # Not in cache — call Claude API
        try:
            content = fetch_article_content(article["url"])
            if not content:
                content = BeautifulSoup(article["description"], "html.parser").get_text()

            result = generate_summary(
                client=client,
                model=config["model"],
                feed_name=article["feed_name"],
                feed_author=article["feed_author"],
                title=article["title"],
                content=content,
                published=article["published"],
            )
            article["summary"] = result.get("summary", "")
            article["takeaways"] = [f"- {t}" for t in result.get("takeaways", [])]
            article["author"] = result.get("author", article["feed_author"])
            article["date"] = article["published"]
            api_calls += 1
            log.info(f"Summarized (API): {article['title']}")

        except Exception as e:
            log.error(f"Failed to summarize '{article['title']}': {e}")
            article["summary"] = article.get("description", "")
            article["takeaways"] = []
            article["author"] = article["feed_author"]
            article["date"] = article["published"]

        # Brief pause between API calls to reduce overload risk
        if i < len(articles) - 1:
            time.sleep(1)

    log.info(f"Summary sources: {cache_hits} cached, {api_calls} API calls")

    # Remove articles with no summary
    articles = [a for a in articles if a.get("summary")]

    if not articles:
        log.info("No articles with summaries. Skipping digest.")
        return

    # Rank and format
    try:
        ranking = generate_ranking(client, config["model"], articles)
    except Exception as e:
        log.warning(f"Failed to rank articles via AI: {e}")
        log.info("Using default chronological ordering instead")
        ranking = [
            {"index": i, "rank": i + 1, "relevance": "", "must_read": i < 3}
            for i in range(len(articles))
        ]

    today = datetime.now()
    week_start = (today - timedelta(days=7)).strftime("%b %d")
    week_end = today.strftime("%b %d, %Y")

    digest_content = format_digest(articles, ranking, week_start, week_end, feeds)

    # Save digest as markdown note
    digest_dir = NOTES_DIR / "Digests"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest_date = today.strftime("%Y-%m-%d")
    digest_path = digest_dir / f"{digest_date} Weekly PM Digest.md"
    digest_path.write_text(digest_content, encoding="utf-8")
    log.info(f"Saved digest: {digest_path.relative_to(SCRIPT_DIR)}")

    # Send email
    send_digest_email(config, digest_content, week_end)
    log.info("Done.")


if __name__ == "__main__":
    main()
