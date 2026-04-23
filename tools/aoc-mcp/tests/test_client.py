"""Tests for aoc_mcp.client — httpx client + session-expiry sniff + rate limiting."""
import json
import time
from pathlib import Path

import httpx
import pytest

from aoc_mcp.client import AocClient, detect_login_form
from aoc_mcp.errors import SessionExpired
from aoc_mcp import config

FIXTURES = Path(__file__).parent / "fixtures"


def test_detect_login_form_positive():
    html = (FIXTURES / "login-redirect-response.html").read_text()
    assert detect_login_form(html, final_url="https://example.com/page") is True


def test_detect_login_form_negative():
    html = (FIXTURES / "authenticated-article-response.html").read_text()
    assert detect_login_form(html, final_url="https://example.com/page") is False


def test_detect_login_form_redirect_to_login():
    # Short body, but URL signals login redirect
    html = "<html><body>redirecting...</body></html>"
    assert detect_login_form(
        html,
        final_url="https://www.theartofcoachingvolleyball.com/login?redirect_to=..."
    ) is True


def test_client_raises_session_expired_when_session_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "nope.json")
    with pytest.raises(SessionExpired):
        AocClient()


def test_client_loads_cookies_from_session_file(tmp_path, monkeypatch):
    """AocClient loads Playwright storage_state.json cookies into httpx."""
    session = {
        "cookies": [
            {
                "name": "wordpress_logged_in_abc",
                "value": "test-value",
                "domain": ".theartofcoachingvolleyball.com",
                "path": "/",
                "expires": -1,
            }
        ],
        "origins": [],
    }
    session_file = tmp_path / "session.json"
    session_file.write_text(json.dumps(session))
    monkeypatch.setattr(config, "SESSION_FILE", session_file)

    client = AocClient()
    cookie_names = [c.name for c in client._http.cookies.jar]
    assert "wordpress_logged_in_abc" in cookie_names


def test_rate_limit_enforced(tmp_path, monkeypatch):
    """Two calls in a row must be spaced at least REQUEST_MIN_INTERVAL_S apart."""
    session = {"cookies": [], "origins": []}
    session_file = tmp_path / "session.json"
    session_file.write_text(json.dumps(session))
    monkeypatch.setattr(config, "SESSION_FILE", session_file)
    monkeypatch.setattr(config, "REQUEST_MIN_INTERVAL_S", 0.2)

    client = AocClient()
    # Stub the actual HTTP call
    client._http.get = lambda *a, **kw: httpx.Response(200, text="<html></html>",
                                                       request=httpx.Request("GET", a[0]))

    start = time.monotonic()
    client.get("https://example.com/a")
    client.get("https://example.com/b")
    elapsed = time.monotonic() - start
    assert elapsed >= 0.2, f"rate limit not enforced: elapsed={elapsed}"


def test_detect_login_form_does_not_false_positive_on_login_prefixed_slug():
    """A URL containing /login-xyz (a slug that starts with 'login') must NOT be sniffed as login."""
    assert detect_login_form(
        body="<html><body>real article</body></html>",
        final_url="https://www.theartofcoachingvolleyball.com/login-strategies-for-captains/"
    ) is False
