"""Tests for ingest_cloud.py utility functions."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure the project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest_cloud import (
    format_note,
    load_seen,
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
