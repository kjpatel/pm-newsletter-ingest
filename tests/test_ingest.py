"""Tests for ingest_cloud.py utility functions."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Ensure the project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest_cloud import (
    fetch_article_content,
    format_note,
    load_seen,
    process_feed,
    sanitize_filename,
    save_seen,
)


class TestSanitizeFilename:
    def test_removes_illegal_characters(self):
        assert sanitize_filename('What "PM" Means: A Guide') == "What PM Means A Guide"

    def test_collapses_whitespace(self):
        assert sanitize_filename("too   many   spaces") == "too many spaces"

    def test_truncates_long_titles(self):
        title = "A" * 100
        result = sanitize_filename(title)
        assert len(result) <= 80

    def test_truncates_at_word_boundary(self):
        title = "word " * 20  # 100 chars
        result = sanitize_filename(title)
        assert len(result) <= 80
        assert not result.endswith(" ")

    def test_strips_whitespace(self):
        assert sanitize_filename("  hello  ") == "hello"

    def test_removes_all_special_chars(self):
        assert sanitize_filename("a<b>c:d/e\\f|g?h*i") == "abcdefghi"


class TestLoadSaveSeen:
    def test_load_returns_empty_for_missing_file(self, tmp_path):
        with patch("ingest_cloud.SCRIPT_DIR", tmp_path):
            (tmp_path / "seen").mkdir()
            result = load_seen("nonexistent.json")
            assert result == []

    def test_save_and_load_roundtrip(self, tmp_path):
        with patch("ingest_cloud.SCRIPT_DIR", tmp_path):
            (tmp_path / "seen").mkdir()
            urls = ["https://example.com/1", "https://example.com/2"]
            save_seen("test_seen.json", urls)
            loaded = load_seen("test_seen.json")
            assert loaded == urls

    def test_save_overwrites(self, tmp_path):
        with patch("ingest_cloud.SCRIPT_DIR", tmp_path):
            (tmp_path / "seen").mkdir()
            save_seen("test.json", ["a"])
            save_seen("test.json", ["b", "c"])
            assert load_seen("test.json") == ["b", "c"]


class TestFormatNote:
    def test_contains_all_sections(self):
        result_data = {
            "author": "Test Author",
            "summary": "This is the summary.",
            "takeaways": ["**Bold** insight one", "**Bold** insight two"],
            "related": ["Note A", "Note B"],
        }
        note = format_note("Test Title", "https://example.com", "Mar 01, 2026", "Test Feed", result_data)

        assert "# Test Title" in note
        assert "## Summary" in note
        assert "## Key Takeaways" in note
        assert "## Related" in note
        assert "[[Note A]]" in note
        assert "[[Note B]]" in note
        assert "This is the summary." in note
        assert "[Test Feed](https://example.com)" in note
        assert "Test Author" in note
        assert "Mar 01, 2026" in note

    def test_handles_empty_takeaways(self):
        result_data = {"author": "A", "summary": "S", "takeaways": [], "related": []}
        note = format_note("T", "http://x.com", "Jan 01", "F", result_data)
        assert "## Key Takeaways" in note

    def test_handles_missing_fields(self):
        note = format_note("T", "http://x.com", "Jan 01", "F", {})
        assert "Unknown" in note  # default author


class TestFetchArticleContent:
    """Tests for fetch_article_content() — HTML extraction and error handling."""

    @patch("ingest_cloud.httpx.get")
    def test_extracts_article_text(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = '<html><body><article><p>Hello world</p></article></body></html>'
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_article_content("https://example.com/post")
        assert "Hello world" in result

    @patch("ingest_cloud.httpx.get")
    def test_strips_script_and_style_tags(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = (
            '<html><body><article>'
            '<p>Real content</p>'
            '<script>alert("x")</script>'
            '<style>.x{color:red}</style>'
            '</article></body></html>'
        )
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_article_content("https://example.com/post")
        assert "Real content" in result
        assert "alert" not in result
        assert "color:red" not in result

    @patch("ingest_cloud.httpx.get")
    def test_returns_empty_on_network_error(self, mock_get):
        import httpx
        mock_get.side_effect = httpx.HTTPError("Connection refused")

        result = fetch_article_content("https://example.com/fail")
        assert result == ""

    @patch("ingest_cloud.httpx.get")
    def test_truncates_long_content(self, mock_get):
        mock_resp = MagicMock()
        long_text = "word " * 5000  # ~25000 chars
        mock_resp.text = f'<html><body><article><p>{long_text}</p></article></body></html>'
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_article_content("https://example.com/long")
        assert len(result) <= 8100  # 8000 + truncation marker
        assert "[... truncated]" in result

    @patch("ingest_cloud.httpx.get")
    def test_falls_back_to_full_page_text(self, mock_get):
        """When no article/content div found, extracts all page text."""
        mock_resp = MagicMock()
        mock_resp.text = '<html><body><div>Fallback text</div></body></html>'
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_article_content("https://example.com/noarticle")
        assert "Fallback text" in result


class TestProcessFeed:
    """Tests for process_feed() — feed processing orchestration."""

    def _make_feed_config(self):
        return {
            "name": "Test Feed",
            "url": "https://example.com/rss",
            "seen_file": "test_feed.json",
            "author": "Test Author",
        }

    def _make_article(self, title="Test Article", url="https://example.com/1",
                      published_iso="2026-03-10"):
        return {
            "title": title,
            "url": url,
            "published": "Mar 10, 2026",
            "published_iso": published_iso,
            "description": "<p>Desc</p>",
        }

    @patch("ingest_cloud.save_seen")
    @patch("ingest_cloud.generate_summary")
    @patch("ingest_cloud.fetch_article_content")
    @patch("ingest_cloud.fetch_feed")
    @patch("ingest_cloud.load_seen")
    @patch("ingest_cloud.NOTES_DIR")
    def test_skips_already_seen_articles(self, mock_notes_dir, mock_load_seen,
                                         mock_fetch_feed, mock_fetch_content,
                                         mock_gen_summary, mock_save_seen, tmp_path):
        mock_notes_dir.__truediv__ = lambda self, x: tmp_path / x
        mock_load_seen.return_value = ["https://example.com/1"]
        mock_fetch_feed.return_value = [self._make_article()]

        result = process_feed(self._make_feed_config(), {"model": "test"}, MagicMock(), [])

        assert result == 0
        mock_fetch_content.assert_not_called()
        mock_gen_summary.assert_not_called()

    @patch("ingest_cloud.save_seen")
    @patch("ingest_cloud.generate_summary")
    @patch("ingest_cloud.fetch_article_content")
    @patch("ingest_cloud.fetch_feed")
    @patch("ingest_cloud.load_seen")
    def test_writes_note_for_new_article(self, mock_load_seen, mock_fetch_feed,
                                          mock_fetch_content, mock_gen_summary,
                                          mock_save_seen, tmp_path):
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()

        mock_load_seen.return_value = []
        mock_fetch_feed.return_value = [self._make_article()]
        mock_fetch_content.return_value = "Article body text"
        mock_gen_summary.return_value = {
            "author": "Test Author",
            "summary": "A summary.",
            "takeaways": ["Point one"],
            "related": [],
        }

        with patch("ingest_cloud.NOTES_DIR", notes_dir), \
             patch("ingest_cloud.SCRIPT_DIR", tmp_path):
            result = process_feed(self._make_feed_config(), {"model": "test"}, MagicMock(), [])

        assert result == 1
        mock_save_seen.assert_called_once()
        saved_urls = mock_save_seen.call_args[0][1]
        assert "https://example.com/1" in saved_urls

    @patch("ingest_cloud.save_seen")
    @patch("ingest_cloud.generate_summary")
    @patch("ingest_cloud.fetch_article_content")
    @patch("ingest_cloud.fetch_feed")
    @patch("ingest_cloud.load_seen")
    def test_continues_on_article_failure(self, mock_load_seen, mock_fetch_feed,
                                           mock_fetch_content, mock_gen_summary,
                                           mock_save_seen, tmp_path):
        """If one article fails, the rest should still be processed."""
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()

        mock_load_seen.return_value = []
        mock_fetch_feed.return_value = [
            self._make_article(title="Bad Article", url="https://example.com/bad"),
            self._make_article(title="Good Article", url="https://example.com/good"),
        ]
        mock_fetch_content.return_value = "Content"
        mock_gen_summary.side_effect = [
            Exception("Claude API error"),
            {"author": "A", "summary": "S", "takeaways": [], "related": []},
        ]

        with patch("ingest_cloud.NOTES_DIR", notes_dir), \
             patch("ingest_cloud.SCRIPT_DIR", tmp_path):
            result = process_feed(self._make_feed_config(), {"model": "test"}, MagicMock(), [])

        assert result == 1  # only the second article succeeded

    @patch("ingest_cloud.save_seen")
    @patch("ingest_cloud.fetch_feed")
    @patch("ingest_cloud.load_seen")
    def test_returns_zero_when_no_new_articles(self, mock_load_seen,
                                                mock_fetch_feed, mock_save_seen):
        mock_load_seen.return_value = []
        mock_fetch_feed.return_value = []

        result = process_feed(self._make_feed_config(), {"model": "test"}, MagicMock(), [])

        assert result == 0
        mock_save_seen.assert_not_called()
