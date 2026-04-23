"""Tests for aoc_mcp.extract — article HTML → ArticleResult."""
from pathlib import Path

import pytest

from aoc_mcp.extract import parse_article
from aoc_mcp.errors import ParserFailed

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_ARTICLE = FIXTURES / "live-article-kiraly-4-keys-forearm-pass.html"


def test_parse_article_basic_shape():
    """Parsing a live AOC article yields a populated ArticleResult."""
    html = LIVE_ARTICLE.read_text(encoding="utf-8")
    result = parse_article(
        html,
        url="https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/",
    )
    assert result.title, "title must not be empty"
    assert result.url.endswith("/karch-kiralys-4-keys-to-the-forearm-pass/")
    assert result.markdown, "markdown body must not be empty"
    assert result.word_count > 100, (
        f"expected substantive article (>100 words), got {result.word_count}"
    )


def test_parse_article_title_matches_fixture_h1():
    """The extracted title matches the page's <h1 class=entry-title> text."""
    html = LIVE_ARTICLE.read_text(encoding="utf-8")
    result = parse_article(html, url="https://example.com/x")
    # Title should mention "Karch" or "forearm" or "pass"
    assert any(
        kw.lower() in result.title.lower()
        for kw in ("karch", "forearm", "pass", "kiraly")
    ), f"title {result.title!r} doesn't match expected article"


def test_parse_article_strips_site_chrome():
    """Markdown body must NOT include site nav, header, footer artifacts."""
    html = LIVE_ARTICLE.read_text(encoding="utf-8")
    result = parse_article(html, url="https://example.com/x")
    forbidden = ["<nav", "<header", "<footer", "menu-primary", "site-header"]
    for f in forbidden:
        assert f not in result.markdown.lower(), (
            f"site chrome token {f!r} leaked into markdown"
        )


def test_parse_article_handles_empty_html_with_parser_failed():
    with pytest.raises(ParserFailed):
        parse_article("<html><body></body></html>", url="https://example.com/empty")


def test_parse_article_attaches_url():
    html = LIVE_ARTICLE.read_text(encoding="utf-8")
    url = "https://www.theartofcoachingvolleyball.com/foo/"
    result = parse_article(html, url=url)
    assert result.url == url
