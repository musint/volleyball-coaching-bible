"""Tests for aoc_mcp.errors — structured error hierarchy."""
from aoc_mcp.errors import (
    AocError,
    SessionExpired,
    NotFound,
    RateLimited,
    UpstreamError,
    ParserFailed,
    UnsupportedProvider,
    UnknownTopic,
)


def test_all_errors_inherit_from_aoc_error():
    """Every specific error must subclass AocError for a single catch."""
    for cls in [SessionExpired, NotFound, RateLimited, UpstreamError,
                ParserFailed, UnsupportedProvider, UnknownTopic]:
        assert issubclass(cls, AocError), f"{cls.__name__} must subclass AocError"


def test_session_expired_carries_reauth_message():
    e = SessionExpired()
    assert "python -m aoc_mcp.auth" in str(e)


def test_not_found_carries_url():
    e = NotFound(url="https://example.com/foo")
    assert "https://example.com/foo" in str(e)
    assert e.url == "https://example.com/foo"


def test_parser_failed_carries_url_and_snippet():
    e = ParserFailed(url="https://example.com/x", snippet="<html>broken</html>")
    assert e.url == "https://example.com/x"
    assert e.snippet == "<html>broken</html>"


def test_unknown_topic_lists_known_topics():
    e = UnknownTopic(topic="foo", known_topics=["passing", "setting"])
    assert e.topic == "foo"
    assert "passing" in e.known_topics
    assert "passing" in str(e)
