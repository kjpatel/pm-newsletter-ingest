"""Tests for digest_cloud.py utility functions."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from digest_cloud import (
    build_feed_homepage_map,
    format_digest,
    load_cached_notes,
    markdown_to_html,
)


class TestBuildFeedHomepageMap:
    def test_strips_feed_suffix(self):
        feeds = [{"name": "Test", "url": "https://example.com/feed"}]
        result = build_feed_homepage_map(feeds)
        assert result == {"Test": "https://example.com"}

    def test_strips_index_xml(self):
        feeds = [{"name": "Blog", "url": "https://blog.com/index.xml"}]
        result = build_feed_homepage_map(feeds)
        assert result == {"Blog": "https://blog.com"}

    def test_multiple_feeds(self):
        feeds = [
            {"name": "A", "url": "https://a.com/feed"},
            {"name": "B", "url": "https://b.com/feed/"},
        ]
        result = build_feed_homepage_map(feeds)
        assert result["A"] == "https://a.com"
        assert result["B"] == "https://b.com"


class TestFormatDigest:
    def _make_articles(self, n=3):
        return [
            {
                "title": f"Article {i}",
                "url": f"https://example.com/{i}",
                "feed_name": "Test Feed",
                "author": "Author",
                "date": "Mar 01, 2026",
                "summary": f"Summary for article {i}.",
                "takeaways": [f"- Takeaway {i}"],
            }
            for i in range(n)
        ]

    def _make_ranking(self, n=3):
        return [
            {"index": i, "rank": i + 1, "relevance": "Relevant", "must_read": i < 1}
            for i in range(n)
        ]

    def test_contains_header(self):
        articles = self._make_articles()
        ranking = self._make_ranking()
        result = format_digest(articles, ranking, "Feb 28", "Mar 07, 2026")
        assert "Weekly PM Digest" in result
        assert "3 new articles" in result

    def test_must_read_section(self):
        articles = self._make_articles()
        ranking = self._make_ranking()
        result = format_digest(articles, ranking, "Feb 28", "Mar 07, 2026")
        assert "## Must-Read" in result

    def test_all_articles_listed(self):
        articles = self._make_articles()
        ranking = self._make_ranking()
        result = format_digest(articles, ranking, "Feb 28", "Mar 07, 2026")
        for a in articles:
            assert a["title"] in result


class TestMarkdownToHtml:
    def test_converts_h1(self):
        html = markdown_to_html("# Hello")
        assert "<h1>Hello</h1>" in html

    def test_converts_h2(self):
        html = markdown_to_html("## Section")
        assert "<h2>Section</h2>" in html

    def test_converts_blockquote(self):
        html = markdown_to_html("> Quote text")
        assert "<blockquote" in html
        assert "Quote text" in html

    def test_converts_table(self):
        md = "| Feed | Count |\n|------|-------|\n| Test | 5 |"
        html = markdown_to_html(md)
        assert "<table" in html
        assert "Test" in html

    def test_converts_markdown_links(self):
        html = markdown_to_html("### 1. [Title](https://example.com)")
        assert '<a href="https://example.com">Title</a>' in html

    def test_wraps_in_styled_div(self):
        html = markdown_to_html("# Test")
        assert html.startswith("<div")
        assert html.endswith("</div>")


class TestLoadCachedNotes:
    def test_returns_empty_when_no_notes_dir(self, tmp_path):
        with patch("digest_cloud.NOTES_DIR", tmp_path / "nonexistent"):
            result = load_cached_notes()
            assert result == {}

    def test_loads_valid_note(self, tmp_path):
        feed_dir = tmp_path / "Test Feed"
        feed_dir.mkdir(parents=True)

        note = """# Test Article

**Source**: [Test Feed](https://example.com/1)
**Author**: Author Name | **Date**: Mar 01, 2026

---

## Summary

This is the summary.

## Key Takeaways

- **Bold** takeaway one
- **Bold** takeaway two

## Related

- [[Note A]]
"""
        (feed_dir / "2026-03-05 Test Article.md").write_text(note)

        with patch("digest_cloud.NOTES_DIR", tmp_path):
            result = load_cached_notes(days=7)

        assert "Test Article" in result
        assert result["Test Article"]["summary"] == "This is the summary."
        assert len(result["Test Article"]["takeaways"]) == 2

    def test_skips_digest_directory(self, tmp_path):
        digest_dir = tmp_path / "Digests"
        digest_dir.mkdir()
        (digest_dir / "2026-03-05 Weekly PM Digest.md").write_text("# Digest\n\n## Summary\n\nStuff")

        with patch("digest_cloud.NOTES_DIR", tmp_path):
            result = load_cached_notes(days=7)

        assert len(result) == 0
