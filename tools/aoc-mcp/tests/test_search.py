"""Tests for aoc_mcp.search — search results parser."""
from pathlib import Path

from aoc_mcp.search import parse_search_results

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_SEARCH = FIXTURES / "live-search-karch.html"


def test_parse_search_returns_at_least_one_hit():
    html = LIVE_SEARCH.read_text(encoding="utf-8")
    result = parse_search_results(html, limit=10)
    assert result.total_returned >= 1, "expected at least one search hit"
    assert len(result.hits) == result.total_returned


def test_search_hits_have_title_and_url():
    html = LIVE_SEARCH.read_text(encoding="utf-8")
    result = parse_search_results(html, limit=10)
    for hit in result.hits:
        assert hit.title, "hit title must not be empty"
        assert hit.url.startswith("http"), f"hit url {hit.url!r} must be absolute"


def test_search_respects_limit():
    html = LIVE_SEARCH.read_text(encoding="utf-8")
    result = parse_search_results(html, limit=3)
    assert result.total_returned <= 3


def test_search_karch_results_mention_karch():
    """A search for 'karch' should return hits whose titles/snippets mention him."""
    html = LIVE_SEARCH.read_text(encoding="utf-8")
    result = parse_search_results(html, limit=10)
    matches = [
        h for h in result.hits
        if "karch" in h.title.lower() or "karch" in (h.snippet or "").lower()
    ]
    assert len(matches) >= 1, "expected at least one karch-mentioning hit"
