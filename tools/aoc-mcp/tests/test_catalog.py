"""Tests for aoc_mcp.catalog — topic listing."""
from pathlib import Path

import pytest

from aoc_mcp.catalog import parse_category_page
from aoc_mcp.errors import UnknownTopic

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_CATEGORY = FIXTURES / "live-category-passing-drills.html"


def test_parse_category_returns_items():
    html = LIVE_CATEGORY.read_text(encoding="utf-8")
    result = parse_category_page(html, limit=20)
    assert result.total_returned >= 1


def test_parse_category_items_have_title_and_url():
    html = LIVE_CATEGORY.read_text(encoding="utf-8")
    result = parse_category_page(html, limit=20)
    for hit in result.hits:
        assert hit.title
        assert hit.url.startswith("http")


def test_list_recent_unknown_topic():
    from aoc_mcp.catalog import list_recent
    with pytest.raises(UnknownTopic):
        list_recent(topic="not-a-real-topic-asdf", limit=5)
