# PM Newsletter Auto-Ingest

Automatically fetches new articles from 20 PM and VC newsletters, generates AI-powered summaries and key takeaways using Claude, writes them as organized notes to your Obsidian vault, and delivers a ranked weekly email digest.

Built for product managers who want to stay on top of industry content without the manual effort of reading, summarizing, and filing every article.

## How It Works

```
                  ┌─────────────────────────────────────┐
                  │         Daily: ingest.py             │
                  │                                      │
  RSS Feeds ──►   │  Fetch Article ──► Claude AI ──►     │  ──► Obsidian Notes
  (20 sources)    │                    Summary +         │
                  │                    Takeaways         │
                  └─────────────────────────────────────┘

                  ┌─────────────────────────────────────┐
                  │         Weekly: digest.py            │
                  │                                      │
  Obsidian    ──► │  Collect Week's Notes ──► Claude AI  │  ──► Email Digest
  Notes           │                          Ranking     │
                  └─────────────────────────────────────┘

                  ┌─────────────────────────────────────┐
                  │    Weekly: digest_cloud.py           │
                  │    (GitHub Actions)                  │
  RSS Feeds ──►   │  Fetch + Summarize ──► Claude AI    │  ──► Email Digest
  (20 sources)    │                        Ranking      │
                  └─────────────────────────────────────┘
```

### Article Ingestion (`ingest.py`)

1. Parses RSS feeds from 20 configured newsletters
2. Detects new articles by comparing against per-feed seen trackers
3. Fetches the full article content (not just the RSS excerpt)
4. Calls Claude to generate a structured summary, key takeaways, author attribution, and cross-links to existing notes
5. Writes a formatted markdown note to the appropriate Obsidian vault folder
6. Tracks processed articles to prevent duplicates

### Weekly Digest — Local (`digest.py`)

1. Scans the Obsidian vault for all article notes from the past 7 days
2. Parses each note to extract title, author, date, source, summary, and key takeaways
3. Calls Claude to rank all articles by strategic relevance (tailored to your role/priorities)
4. Generates a digest with a "Must-Read" section (top 3) and a full ranked list
5. Saves the digest as an Obsidian note and sends it as a styled HTML email via Resend

### Weekly Digest — Cloud (`digest_cloud.py`)

A self-contained version that runs in GitHub Actions with no local dependencies:

1. Fetches all 20 RSS feeds and filters to articles from the past 7 days
2. Fetches full article content and generates summaries via Claude
3. Ranks all articles by strategic relevance
4. Sends a styled HTML digest email via Resend
5. Runs automatically every Saturday via GitHub Actions cron

## AI Features

### Summaries & Key Takeaways

Each article is processed by Claude Haiku, which generates:

- **Summary** — 1-2 sentence core argument of the article
- **Key Takeaways** — 3-5 actionable insights, each with a bolded lead phrase
- **Author Attribution** — Handles guest authors (e.g., "Lenny Rachitsky (featuring Guest Name)")
- **Related Notes** — 2-3 Obsidian `[[wikilinks]]` to existing notes in your vault

### AI-Powered Ranking

The weekly digest uses Claude to rank articles by relevance to a VP of Product at a Series C B2B SaaS startup, scoring against five strategic priorities:

1. Scaling a product organization
2. Product-led growth
3. AI/ML product strategy
4. Enterprise product management
5. Strategic roadmapping

Each article receives a relevance phrase explaining why it matters, and the top 3 are flagged as "Must-Read."

## Example Output

### Article Note

```markdown
# How to Price AI Products: The Complete Guide for PMs

**Source**: [Product Growth](https://www.news.aakashg.com/p/how-to-price-ai-products)
**Author**: Aakash Gupta & Moe Ali | **Date**: Feb 26, 2026

---

## Summary

A comprehensive breakdown of 6 pricing models for AI products...

## Key Takeaways

- **Six pricing models**: Hybrid tiered subscriptions, usage-based...
- **Your best users are your most expensive users** — every AI interaction...

## Related

- [[AI Evals Explained Simply]]
- [[PM OS for PMs]]
```

### Weekly Digest Email

The digest arrives as a styled email with:

- **Must-Read** section highlighting the top 3 articles with summaries and takeaways
- **Full ranked list** of all articles from the week with relevance context
- Links back to the original articles

## Configured Feeds

| # | Feed | Author |
|---|------|--------|
| 1 | [Product Growth](https://www.news.aakashg.com) | Aakash Gupta |
| 2 | [Lenny's Newsletter](https://www.lennysnewsletter.com) | Lenny Rachitsky |
| 3 | [Product Compass](https://www.productcompass.pm) | Pawel Huryn |
| 4 | [The Looking Glass](https://lg.substack.com) | Julie Zhuo |
| 5 | [Brian Balfour](https://blog.brianbalfour.com) | Brian Balfour |
| 6 | [Shreyas Doshi](https://shreyasdoshi.substack.com) | Shreyas Doshi |
| 7 | [Elena's Growth Scoop](https://www.elenaverna.com) | Elena Verna |
| 8 | [The Beautiful Mess](https://cutlefish.substack.com) | John Cutler |
| 9 | [Perspectives](https://debliu.substack.com) | Deb Liu |
| 10 | [Department of Product](https://departmentofproduct.substack.com) | Rich Holmes |
| 11 | [Casey Accidental](https://www.caseyaccidental.com) | Casey Winters |
| 12 | [Wes Kao](https://newsletter.weskao.com) | Wes Kao |
| 13 | [SVPG](https://www.svpg.com) | Marty Cagan |
| 14 | [Itamar Gilad](https://itamargilad.com) | Itamar Gilad |
| 15 | [Stratechery](https://stratechery.com) | Ben Thompson |
| 16 | [Sequoia Capital](https://sequoiacap.com) | Sequoia Capital |
| 17 | [Both Sides of the Table](https://bothsidesofthetable.com) | Mark Suster |
| 18 | [Feld Thoughts](https://feld.com) | Brad Feld |
| 19 | [Hunter Walk](https://hunterwalk.com) | Hunter Walk |
| 20 | [Tomasz Tunguz](https://tomtunguz.com) | Tomasz Tunguz |

## Setup

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- An Obsidian vault
- A [Resend API key](https://resend.com/) (optional, for email digest)

### Install

```bash
git clone https://github.com/kjpatel/pm-newsletter-ingest.git
cd pm-newsletter-ingest

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure

1. Copy and edit the environment file:

```bash
cp .env.example .env
# Add your Anthropic API key (required)
# Add your Resend API key (optional, for email digest)
```

2. Edit `config.json` to point to your vault and configure feeds:

```json
{
  "vault_path": "/path/to/your/obsidian/vault",
  "case_studies_path": "PM Craft/Reading Notes",
  "model": "claude-haiku-4-5-20251001",
  "digest_email": {
    "enabled": true,
    "from": "PM Digest <digest@yourdomain.com>",
    "to": ["you@example.com"]
  },
  "feeds": [
    {
      "name": "Product Growth",
      "url": "https://www.news.aakashg.com/feed",
      "author": "Aakash Gupta",
      "seen_file": "seen_product_growth.json"
    }
  ]
}
```

### Run

```bash
source .venv/bin/activate

# Ingest new articles
python3 ingest.py

# Generate and email weekly digest
python3 digest.py
```

## Adding Feeds

Add any Substack newsletter (or any RSS feed) to the `feeds` array in `config.json`:

```json
{
  "name": "Newsletter Name",
  "url": "https://example.com/feed",
  "author": "Author Name",
  "seen_file": "seen_newsletter_name.json"
}
```

The script auto-creates folders as needed in your Obsidian vault.

## Scheduling

### macOS (launchd)

Create plist files at `~/Library/LaunchAgents/`:

**Daily ingestion** (`com.newsletter-ingest.plist`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.newsletter-ingest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/pm-newsletter-ingest/.venv/bin/python3</string>
        <string>/path/to/pm-newsletter-ingest/ingest.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/pm-newsletter-ingest/logs/ingest.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/pm-newsletter-ingest/logs/ingest-error.log</string>
</dict>
</plist>
```

**Weekly digest** (`com.newsletter-digest.plist`) — same structure, with a `Weekday` key (e.g., `1` for Monday).

Then load them:

```bash
launchctl load ~/Library/LaunchAgents/com.newsletter-ingest.plist
launchctl load ~/Library/LaunchAgents/com.newsletter-digest.plist
```

### Linux (cron)

```bash
crontab -e
# Daily ingestion at 8am
0 8 * * * cd /path/to/pm-newsletter-ingest && .venv/bin/python3 ingest.py >> logs/ingest.log 2>&1
# Weekly digest on Mondays at 9am
0 9 * * 1 cd /path/to/pm-newsletter-ingest && .venv/bin/python3 digest.py >> logs/digest.log 2>&1
```

### GitHub Actions (cloud digest)

The cloud digest runs automatically via GitHub Actions — no local machine required.

1. Push this repo to GitHub
2. Add repository secrets in **Settings > Secrets and variables > Actions**:
   - `ANTHROPIC_API_KEY`
   - `RESEND_API_KEY`
3. The workflow runs every Saturday at 9am ET (2pm UTC). You can also trigger it manually from the **Actions** tab.

## Cost

Uses Claude Haiku (~$0.01-0.03 per article). A typical daily run processing 2-3 new articles costs under $0.10. The weekly digest ranking adds a single additional API call.

## License

[MIT](LICENSE)
