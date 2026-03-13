#!/usr/bin/env python3
"""
Cloud-based Weekly PM Digest Generator

Fetches RSS feeds, reuses summaries from the daily ingest (notes/ directory),
ranks articles by relevance using Claude, and sends a weekly digest email
via Resend. Only calls Claude for the ranking step and any articles not
already summarized by ingest_cloud.py.

Designed to run in GitHub Actions.
"""

import argparse
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
        max_tokens=4096,
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
        f"# PM Pulse: Weekly Digest — {week_end}",
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
    """Convert digest markdown to styled HTML email with NyxWorks branding."""
    lines = md.splitlines()
    html = []

    # --- Phase 1: extract header info from the first few lines ---
    title = ""
    subtitle = ""
    header_end = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:]
        elif stripped == "---":
            header_end = idx + 1
            break
        elif stripped:
            subtitle = stripped

    # Parse "32 articles from 13 feeds | Mar 06 – Mar 13, 2026"
    parts = subtitle.split("|")
    article_info = parts[0].strip() if parts else subtitle
    date_range = parts[1].strip() if len(parts) > 1 else ""

    # --- Header ---
    html.append(
        '<div style="background:#0B0F1A;padding:32px 40px 28px;">'
        '<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
        '<td>'
        '<span style="color:#8A5CFF;font-size:24px;font-weight:700;'
        'letter-spacing:-0.5px;">PM Pulse</span>'
        '<span style="color:#7B7F8E;font-size:14px;margin-left:8px;">'
        'by NyxWorks.ai</span>'
        '</td>'
        '<td align="right">'
        f'<span style="color:#7B7F8E;font-size:13px;">{date_range}</span>'
        '</td>'
        '</tr></table>'
        f'<p style="color:#C9CCD6;font-size:14px;margin:12px 0 0;line-height:1.5;">'
        f'{article_info} &mdash; AI-ranked for product leaders</p>'
        '</div>'
    )

    # --- Body ---
    html.append('<div style="padding:32px 40px;">')

    section = None  # "must_read" or "all_articles"
    in_card = False

    for line in lines[header_end:]:
        stripped = line.strip()

        if not stripped:
            continue

        # --- Separators ---
        if stripped == "---":
            if in_card and section == "must_read":
                html.append('</div>')
                in_card = False
            continue

        # --- Section headers ---
        if stripped == "## Must-Read":
            section = "must_read"
            html.append(
                '<h2 style="font-size:13px;text-transform:uppercase;'
                'letter-spacing:1.5px;color:#5B3FD6;margin:0 0 20px;'
                'font-weight:700;">Must-Read</h2>'
            )
            continue

        if stripped == "## All Articles":
            if in_card:
                html.append('</div>')
                in_card = False
            section = "all_articles"
            html.append(
                '<hr style="border:none;border-top:1px solid #E8E8EC;margin:32px 0;">'
                '<h2 style="font-size:13px;text-transform:uppercase;'
                'letter-spacing:1.5px;color:#7B7F8E;margin:0 0 20px;'
                'font-weight:700;">All Articles</h2>'
            )
            continue

        # ====== Must-Read section ======
        if section == "must_read":
            # Card title: ### 1. [Title](url)
            if stripped.startswith("### "):
                if in_card:
                    html.append('</div>')
                in_card = True
                html.append(
                    '<div style="border-left:3px solid #5B3FD6;padding:16px 20px;'
                    'margin-bottom:24px;background:#FAFAFF;border-radius:0 6px 6px 0;">'
                )
                inner = stripped[4:]
                m = re.match(r'(\d+)\.\s*\[([^\]]+)\]\(([^)]+)\)', inner)
                if m:
                    rank, t, url = m.group(1), m.group(2), m.group(3)
                    html.append(
                        f'<p style="margin:0 0 4px;">'
                        f'<span style="display:inline-block;background:#5B3FD6;color:#fff;'
                        f'font-size:11px;font-weight:600;padding:2px 8px;border-radius:3px;'
                        f'margin-right:8px;">{rank}</span>'
                        f'<a href="{url}" style="color:#5B3FD6;font-size:17px;'
                        f'font-weight:600;text-decoration:none;">{t}</a></p>'
                    )
                else:
                    m2 = re.match(r'(\d+)\.\s*(.*)', inner)
                    if m2:
                        rank, t = m2.group(1), m2.group(2)
                        html.append(
                            f'<p style="margin:0 0 4px;">'
                            f'<span style="display:inline-block;background:#5B3FD6;'
                            f'color:#fff;font-size:11px;font-weight:600;padding:2px 8px;'
                            f'border-radius:3px;margin-right:8px;">{rank}</span>'
                            f'<span style="color:#1a1a1a;font-size:17px;'
                            f'font-weight:600;">{t}</span></p>'
                        )
                continue

            # Metadata: *Feed — Author — Date*
            if stripped.startswith("*") and not stripped.startswith("**"):
                text = re.sub(r"\*(.+?)\*", r"\1", stripped)
                html.append(
                    f'<p style="margin:4px 0 12px;font-size:13px;color:#7B7F8E;">'
                    f'{text}</p>'
                )
                continue

            # Why it matters
            if stripped.startswith("**Why it matters**"):
                text = stripped.replace("**Why it matters**:", "").strip()
                html.append(
                    f'<p style="margin:0 0 12px;font-size:14px;color:#555;'
                    f'font-weight:500;font-style:italic;">Why it matters: {text}</p>'
                )
                continue

            # Read article → button
            if re.match(r"^\[Read article", stripped):
                url_m = re.search(r'\(([^)]+)\)', stripped)
                url = url_m.group(1) if url_m else "#"
                html.append(
                    f'<div style="margin-top:16px;">'
                    f'<a href="{url}" style="display:inline-block;background:#5B3FD6;'
                    f'color:#fff;font-size:13px;font-weight:600;text-decoration:none;'
                    f'padding:8px 20px;border-radius:5px;">Read article &rarr;</a></div>'
                )
                continue

            # Takeaway bullets
            if stripped.startswith("- "):
                text = stripped[2:]
                text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                html.append(
                    f'<p style="margin:0 0 4px;padding-left:16px;font-size:14px;'
                    f'color:#444;line-height:1.6;">&bull; {text}</p>'
                )
                continue

            # Summary / body text
            text = _md_links(stripped)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            html.append(
                f'<p style="margin:0 0 12px;font-size:15px;color:#333;'
                f'line-height:1.6;">{text}</p>'
            )
            continue

        # ====== All Articles section ======
        if section == "all_articles":
            # Article header: **4.** [Title](url) — *Feed* · Date
            if (
                stripped.startswith("**")
                and ".**" in stripped
                and stripped[2:3].isdigit()
            ):
                if in_card:
                    html.append('</div>')
                in_card = True
                html.append(
                    '<div style="padding:16px 0;border-bottom:1px solid #F0F0F4;">'
                )
                m = re.match(
                    r'\*\*(\d+)\.\*\*\s*\[([^\]]+)\]\(([^)]+)\)\s*—\s*(.*)',
                    stripped,
                )
                if m:
                    rank, t, url, meta = (
                        m.group(1), m.group(2), m.group(3), m.group(4),
                    )
                    meta = re.sub(r"\*(.+?)\*", r"\1", meta)
                    html.append(
                        f'<p style="margin:0 0 4px;">'
                        f'<span style="color:#7B7F8E;font-size:13px;font-weight:600;'
                        f'margin-right:6px;">{rank}.</span>'
                        f'<a href="{url}" style="color:#5B3FD6;font-size:15px;'
                        f'font-weight:500;text-decoration:none;">{t}</a>'
                        f'<span style="color:#7B7F8E;font-size:13px;"> &mdash; '
                        f'{meta}</span></p>'
                    )
                else:
                    # No link or unexpected format — fallback
                    text = _md_links(stripped)
                    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
                    html.append(f'<p style="margin:0 0 4px;">{text}</p>')
                continue

            # Takeaway bullets
            if stripped.startswith("- "):
                text = stripped[2:]
                text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                html.append(
                    f'<p style="margin:0 0 3px;padding-left:16px;font-size:13px;'
                    f'color:#555;line-height:1.5;">&bull; {text}</p>'
                )
                continue

            # Summary text
            text = _md_links(stripped)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            html.append(
                f'<p style="margin:6px 0 10px;font-size:14px;color:#555;'
                f'line-height:1.5;">{text}</p>'
            )
            continue

    # Close any open card
    if in_card:
        html.append('</div>')

    # Close body
    html.append('</div>')

    # --- Footer ---
    html.append(
        '<div style="background:#F7F7FA;padding:24px 40px;'
        'border-top:1px solid #E8E8EC;">'
        '<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
        '<td>'
        '<span style="color:#5B3FD6;font-size:14px;font-weight:600;">PM Pulse</span>'
        '<span style="color:#7B7F8E;font-size:13px;">'
        ' &mdash; AI-curated PM insights, weekly</span>'
        '</td>'
        '<td align="right">'
        '<a href="{{unsub_url}}" style="color:#7B7F8E;font-size:12px;'
        'text-decoration:none;">Unsubscribe</a>'
        '</td>'
        '</tr></table>'
        '</div>'
    )

    body = "\n".join(html)
    return (
        '<div style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,'
        'Helvetica,Arial,sans-serif;max-width:700px;margin:0 auto;'
        f'background:#ffffff;">{body}</div>'
    )


def fetch_audience_contacts(audience_id: str) -> list[str]:
    """Fetch subscribed email addresses from a Resend audience."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key or not audience_id:
        return []

    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.resend.com/audiences/{audience_id}/contacts"
    emails: list[str] = []

    while url:
        resp = httpx.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for contact in data.get("data", []):
            if not contact.get("unsubscribed", False):
                emails.append(contact["email"])

        # Cursor-based pagination
        next_cursor = data.get("next")
        url = (
            f"https://api.resend.com/audiences/{audience_id}/contacts"
            f"?starting_after={next_cursor}"
            if next_cursor
            else None
        )

    return emails


def send_digest_email(config: dict, digest_content: str, week_range: str) -> None:
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

    # Merge hardcoded config recipients with Resend audience contacts
    config_recipients = {r.lower() for r in email_config.get("to", [])}
    audience_id = (
        email_config.get("resend_audience_id")
        or os.environ.get("RESEND_AUDIENCE_ID", "")
    )
    audience_recipients: set[str] = set()

    if audience_id:
        try:
            audience_recipients = {
                r.lower() for r in fetch_audience_contacts(audience_id)
            }
            log.info(f"Fetched {len(audience_recipients)} audience contact(s)")
        except Exception as e:
            log.warning(f"Failed to fetch audience contacts: {e}")

    all_recipients = sorted(config_recipients | audience_recipients)
    overlap = len(config_recipients & audience_recipients)
    log.info(
        f"Recipients: {len(all_recipients)} total "
        f"({len(config_recipients)} config + {len(audience_recipients)} audience"
        f", {overlap} overlap)"
    )

    if not all_recipients:
        log.warning("No recipients — skipping email")
        return

    # Send individually so each recipient gets a personalized unsubscribe link
    signup_api_url = email_config.get("signup_api_url", "")
    sent = 0
    for recipient in all_recipients:
        unsub_url = f"{signup_api_url}?unsub={recipient}" if signup_api_url else "#"
        personalized_html = html.replace("{{unsub_url}}", unsub_url)
        params = {
            "from": email_config["from"],
            "to": [recipient],
            "subject": f"PM Pulse: Weekly Digest ({week_range})",
            "html": personalized_html,
        }
        try:
            resend.Emails.send(params)
            sent += 1
        except Exception as e:
            log.error(f"Failed to send to {recipient}: {e}")
    log.info(f"Digest sent to {sent}/{len(all_recipients)} recipients")


def main():
    parser = argparse.ArgumentParser(description="Weekly PM Digest Generator")
    parser.add_argument(
        "--to",
        nargs="+",
        help="Override recipient list (e.g. --to alice@example.com bob@example.com)",
    )
    args = parser.parse_args()

    config = load_config()

    if args.to:
        config["digest_email"]["to"] = args.to
        log.info(f"Overriding recipients: {args.to}")

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
    week_range = f"{week_start} – {today.strftime('%b %d, %Y')}"

    digest_content = format_digest(articles, ranking, week_start, week_end, feeds)

    # Save digest as markdown note
    digest_dir = NOTES_DIR / "Digests"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest_date = today.strftime("%Y-%m-%d")
    digest_path = digest_dir / f"{digest_date} PM Pulse Weekly Digest.md"
    digest_path.write_text(digest_content, encoding="utf-8")
    log.info(f"Saved digest: {digest_path.relative_to(SCRIPT_DIR)}")

    # Save latest digest as JSON for welcome emails to new subscribers
    email_config = config.get("digest_email", {})
    latest_path = digest_dir / "latest-digest.json"
    latest_path.write_text(
        json.dumps({
            "subject": f"PM Pulse: Weekly Digest ({week_range})",
            "from": email_config.get("from", ""),
            "html": markdown_to_html(digest_content),
            "date": digest_date,
        }),
        encoding="utf-8",
    )
    log.info("Saved latest-digest.json")

    # Send email (skip if SKIP_EMAIL is set, e.g. for local regen)
    if not os.environ.get("SKIP_EMAIL"):
        send_digest_email(config, digest_content, week_range)
    else:
        log.info("SKIP_EMAIL set — skipping email send")
    log.info("Done.")


if __name__ == "__main__":
    main()
