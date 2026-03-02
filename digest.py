#!/usr/bin/env python3
"""
Weekly PM Digest Generator

Scans recent article notes in the Obsidian vault, ranks them by strategic
relevance using Claude, and writes a weekly digest note.
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import anthropic
import resend

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
ENV_PATH = SCRIPT_DIR / ".env"

# Load .env file if it exists
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
)
log = logging.getLogger(__name__)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def parse_note(path: Path) -> dict | None:
    """Extract title, author, date, summary, and feed from an article note."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    result = {"note_filename": path.stem}

    for line in lines:
        if line.startswith("# ") and "title" not in result:
            result["title"] = line[2:].strip()
        elif line.startswith("**Source**:"):
            match = re.search(r"\[(.+?)\]\((.+?)\)", line)
            if match:
                result["feed_name"] = match.group(1)
                result["url"] = match.group(2)
        elif line.startswith("**Author**:"):
            match = re.match(r"\*\*Author\*\*:\s*(.+?)\s*\|\s*\*\*Date\*\*:\s*(.+)", line)
            if match:
                result["author"] = match.group(1).strip()
                result["date"] = match.group(2).strip()

    # Extract summary — text between "## Summary" and the next "##"
    in_summary = False
    summary_lines = []
    for line in lines:
        if line.strip() == "## Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary and line.strip():
            summary_lines.append(line.strip())

    result["summary"] = " ".join(summary_lines)

    # Extract key takeaways — bullets between "## Key Takeaways" and the next "##"
    in_takeaways = False
    takeaway_lines = []
    for line in lines:
        if line.strip() == "## Key Takeaways":
            in_takeaways = True
            continue
        if in_takeaways and line.startswith("## "):
            break
        if in_takeaways and line.strip().startswith("- "):
            takeaway_lines.append(line.strip())
    result["takeaways"] = takeaway_lines

    # Require at minimum a title and summary
    if "title" in result and result["summary"]:
        return result
    return None


def collect_recent_articles(vault_cs: Path, days: int = 7) -> list[dict]:
    """Find all article notes published in the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    articles = []

    for feed_dir in sorted(vault_cs.iterdir()):
        if not feed_dir.is_dir() or feed_dir.name == "Digests":
            continue

        for md_file in feed_dir.glob("*.md"):
            # Extract date from filename prefix (YYYY-MM-DD)
            match = re.match(r"(\d{4}-\d{2}-\d{2})\s", md_file.name)
            if not match:
                continue

            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if file_date < cutoff:
                continue

            article = parse_note(md_file)
            if article:
                articles.append(article)

    # Sort by date descending (newest first)
    articles.sort(key=lambda a: a.get("note_filename", ""), reverse=True)
    return articles


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


def build_feed_homepage_map(feeds: list[dict]) -> dict[str, str]:
    """Map feed name -> blog homepage URL by stripping /feed suffix from RSS URL."""
    result = {}
    for feed in feeds:
        url = re.sub(r"/feed/?$", "", feed["url"])
        result[feed["name"]] = url
    return result


def format_digest(
    articles: list[dict],
    ranking: list[dict],
    week_start: str,
    week_end: str,
    feeds: list[dict] | None = None,
) -> str:
    """Format the ranked digest as an Obsidian markdown note."""
    feed_homepages = build_feed_homepage_map(feeds) if feeds else {}

    feed_counts = {}
    for a in articles:
        name = a.get("feed_name", "Unknown")
        feed_counts[name] = feed_counts.get(name, 0) + 1

    lines = [
        f"# Weekly PM Digest - {week_end}",
        "",
        f"**{len(articles)} new articles** from {len(feed_counts)} feeds ({week_start} – {week_end})",
        "",
        "| Feed | Count |",
        "|------|-------|",
    ]
    for feed, count in sorted(feed_counts.items()):
        homepage = feed_homepages.get(feed, "")
        feed_cell = f"[{feed}]({homepage})" if homepage else feed
        lines.append(f"| {feed_cell} | {count} |")
    lines.append("")

    # Must-reads
    must_reads = [r for r in ranking if r.get("must_read")]
    if must_reads:
        lines.extend(["---", "", "## Must-Read", ""])
        for r in must_reads:
            a = articles[r["index"]]
            title_link = f"[{a['title']}]({a['url']})" if a.get("url") else a["title"]
            entry = [
                f"### {r['rank']}. {title_link}",
                f"*{a.get('feed_name', '')}* | {a.get('author', '')} | {a.get('date', '')}",
                f"> {a['summary']}",
            ]
            takeaways = a.get("takeaways", [])
            if takeaways:
                entry.append("**Key Takeaways**:")
                for t in takeaways:
                    entry.append(f"  {t}")
            entry.extend([f"**Why it matters**: {r.get('relevance', '')}", ""])
            lines.extend(entry)

    # Full ranked list
    lines.extend(["---", "", "## All Articles (Ranked)", ""])
    for r in ranking:
        a = articles[r["index"]]
        tag = " **MUST-READ**" if r.get("must_read") else ""
        title_link = f"[{a['title']}]({a['url']})" if a.get("url") else a["title"]
        entry = [
            f"{r['rank']}. {title_link} - *{a.get('feed_name', '')}*{tag}",
            f"   {a['summary']}",
        ]
        for t in a.get("takeaways", []):
            entry.append(f"   {t}")
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
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Horizontal rule
        if stripped == "---":
            if in_table:
                html_parts.append("</table>")
                in_table = False
            html_parts.append("<hr>")
            continue

        # Table separator row
        if re.match(r"^\|[-| ]+\|$", stripped):
            continue

        # Table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                html_parts.append('<table style="border-collapse:collapse;margin:10px 0;">')
                tag = "th"
                in_table = True
            else:
                tag = "td"
            row = "".join(
                f'<{tag} style="border:1px solid #ddd;padding:6px 12px;">{_md_links(c)}</{tag}>'
                for c in cells
            )
            html_parts.append(f"<tr>{row}</tr>")
            continue

        if in_table:
            html_parts.append("</table>")
            in_table = False

        # Headers
        if stripped.startswith("### "):
            text = _md_links(stripped[4:])
            html_parts.append(f"<h3>{text}</h3>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            html_parts.append(f"<h1>{stripped[2:]}</h1>")
        # Blockquote
        elif stripped.startswith("> "):
            html_parts.append(
                f'<blockquote style="border-left:3px solid #ccc;padding-left:12px;'
                f'color:#555;margin:5px 0;">{stripped[2:]}</blockquote>'
            )
        # Bold line (like "Why it matters")
        elif stripped.startswith("**") and "**:" in stripped:
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            html_parts.append(f"<p>{text}</p>")
        # Numbered list items
        elif re.match(r"^\d+\.", stripped):
            text = _md_links(stripped)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            html_parts.append(f"<p>{text}</p>")
        # Italics line (feed/author/date)
        elif stripped.startswith("*") and not stripped.startswith("**"):
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", stripped)
            html_parts.append(f"<p style='color:#666;'>{text}</p>")
        # Indented bullet lines (takeaways)
        elif line.startswith("  ") and stripped.startswith("- "):
            text = stripped[2:]
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            html_parts.append(f"<p style='margin-left:20px;margin-top:2px;margin-bottom:2px;color:#444;'>&bull; {text}</p>")
        # Indented summary lines
        elif line.startswith("   ") and stripped:
            text = stripped
            if stripped.startswith("- "):
                text = stripped[2:]
                text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                html_parts.append(f"<p style='margin-left:20px;margin-top:2px;margin-bottom:2px;color:#444;'>&bull; {text}</p>")
            else:
                html_parts.append(f"<p style='margin-left:20px;color:#444;'>{text}</p>")
        # Empty line
        elif not stripped:
            continue
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            html_parts.append(f"<p>{text}</p>")

    if in_table:
        html_parts.append("</table>")

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

    vault_cs = Path(config["vault_path"]) / config["case_studies_path"]

    articles = collect_recent_articles(vault_cs, days=7)
    if not articles:
        log.info("No articles from the past 7 days. Skipping digest.")
        return

    log.info(f"Found {len(articles)} articles from the past 7 days")

    client = anthropic.Anthropic()
    ranking = generate_ranking(client, config["model"], articles)

    today = datetime.now()
    week_start = (today - timedelta(days=7)).strftime("%b %d")
    week_end = today.strftime("%b %d, %Y")

    digest_content = format_digest(articles, ranking, week_start, week_end, config.get("feeds", []))

    digest_dir = vault_cs / "Digests"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest_path = digest_dir / f"{today.strftime('%Y-%m-%d')} Weekly Digest.md"
    digest_path.write_text(digest_content, encoding="utf-8")
    log.info(f"Wrote digest: {digest_path.relative_to(Path(config['vault_path']))}")

    send_digest_email(config, digest_content, week_end)


if __name__ == "__main__":
    main()
