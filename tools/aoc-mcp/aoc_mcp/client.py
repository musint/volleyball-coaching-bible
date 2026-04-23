"""AocClient — httpx-based fetcher with session loading and expiry detection."""
from __future__ import annotations

import json
import re
import time
from typing import Optional

import httpx

from aoc_mcp import config
from aoc_mcp.errors import (
    NotFound,
    RateLimited,
    SessionExpired,
    UpstreamError,
)

_LOGIN_FORM_RE = re.compile(
    r'<form[^>]*id=["\']loginform["\']', re.IGNORECASE
)
_WP_LOGIN_ACTION_RE = re.compile(
    r'action=["\'][^"\']*wp-login\.php', re.IGNORECASE
)
_LOGIN_URL_RE = re.compile(
    r'theartofcoachingvolleyball\.com/(?:wp-login\.php|login)',
    re.IGNORECASE,
)


def detect_login_form(body: str, final_url: str) -> bool:
    """Return True if the response looks like AOC redirected us to login.

    Sniff in order of specificity:
    1. Final URL path includes /login or /wp-login.php
    2. Body contains <form id="loginform" ...>
    3. Body contains action="...wp-login.php"
    """
    if _LOGIN_URL_RE.search(final_url):
        return True
    if _LOGIN_FORM_RE.search(body):
        return True
    if _WP_LOGIN_ACTION_RE.search(body):
        return True
    return False


class AocClient:
    """HTTP client that uses the saved AOC session cookies."""

    def __init__(self) -> None:
        session_file = config.SESSION_FILE
        if not session_file.exists():
            raise SessionExpired(
                f"No session file at {session_file}. "
                "Run `python -m aoc_mcp.auth` from tools/aoc-mcp/."
            )
        try:
            storage_state = json.loads(session_file.read_text())
        except json.JSONDecodeError as e:
            raise SessionExpired(
                f"Session file {session_file} is malformed: {e}. Re-auth."
            ) from e

        cookies = httpx.Cookies()
        for c in storage_state.get("cookies", []):
            cookies.set(
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", ""),
                path=c.get("path", "/"),
            )

        self._http = httpx.Client(
            cookies=cookies,
            headers={"User-Agent": config.USER_AGENT},
            timeout=config.DEFAULT_TIMEOUT_S,
            follow_redirects=True,
        )
        self._last_request_time: float = 0.0

    def _enforce_rate_limit(self) -> None:
        min_interval = config.REQUEST_MIN_INTERVAL_S
        deadline = self._last_request_time + min_interval
        # Loop to handle Windows' coarse timer resolution (~15ms) where a single
        # time.sleep() may return slightly before the requested interval elapses.
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            time.sleep(remaining)

    def get(self, url: str, *, retry_5xx: bool = True) -> httpx.Response:
        """GET a URL with rate-limiting, session-expiry sniff, and one retry on 429/5xx.

        Raises:
          SessionExpired: if response smells like a login redirect
          NotFound: on 404
          RateLimited: on 429 after one retry
          UpstreamError: on 5xx after one retry
        """
        self._enforce_rate_limit()
        self._last_request_time = time.monotonic()
        response = self._http.get(url)

        if response.status_code == 404:
            raise NotFound(url)

        if response.status_code == 429:
            time.sleep(1.0)
            response = self._http.get(url)
            if response.status_code == 429:
                raise RateLimited(url)

        if 500 <= response.status_code < 600 and retry_5xx:
            time.sleep(4.0)
            response = self._http.get(url)
            if 500 <= response.status_code < 600:
                raise UpstreamError(url, response.status_code)

        body = response.text
        final_url = str(response.url)
        if detect_login_form(body, final_url):
            raise SessionExpired()

        return response

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "AocClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
