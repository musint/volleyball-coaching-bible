# AOC MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Python MCP server at `tools/aoc-mcp/` that exposes 4 tools (`aoc_fetch_article`, `aoc_search`, `aoc_list_recent`, `aoc_video_transcript`) for authenticated access to Art of Coaching Volleyball premium content, usable from Claude Code via `.mcp.json` in the parent repo.

**Architecture:** Two-phase design. **Phase A (auth, one-time per session lifetime):** `python -m aoc_mcp.auth` launches headed Chromium via Playwright; user logs into AOC manually; Playwright saves cookies + localStorage to `.session.json` (gitignored). **Phase B (fetch, per-tool-call):** Tools load `.session.json` into an httpx client, fetch target URLs with realistic UA + rate limiting, extract markdown/search-results/video-transcripts, and return structured pydantic models. Playwright re-engages only for video transcript extraction (Vimeo/Wistia captions). Session-expiry is detected by a login-form sniff on every response and surfaced as a structured MCP error.

**Tech Stack:** Python 3.11+ · `mcp` (official SDK) · Playwright (Chromium) · httpx · BeautifulSoup4 · markdownify · pydantic 2 · pytest. Platform: Windows 11 (primary dev target); macOS/Linux paths noted where they differ.

**Spec reference:** `docs/superpowers/specs/2026-04-23-aoc-mcp-design.md`

**Work philosophy:** TDD where possible (fixture-based for parsers). Manual smoke tests for Playwright/MCP-server glue. Real fixtures captured from live AOC via a `discover` subcommand rather than hand-fabricated — avoids "hope-the-selector-is-right" drift. Commit after every task. Two user-interactive checkpoints: **IC1 after Task 5** (user runs auth) and **IC2 after Task 6** (user runs discover to populate fixtures).

---

## Operating conventions (read before executing any task)

### Commit-message format
```
<type>: <short description>

<optional body: Task N - what was produced>
```
Where `<type>` ∈ `feat`, `fix`, `test`, `docs`, `chore`, `refactor`. Example:
- `feat: scaffold aoc-mcp package (Task 1)`
- `test: add session-expiry fixture tests for AocClient (Task 4)`

### Python invocation convention
All `python` commands in this plan assume the **venv has been activated** in the current shell unless explicitly noted otherwise:
- Windows bash (used by the project): `source tools/aoc-mcp/.venv/Scripts/activate`
- Windows cmd/PowerShell alternative: `tools\aoc-mcp\.venv\Scripts\activate`

MCP server commands in `.mcp.json` use the venv's python directly (absolute path) — Claude Code does NOT inherit venv state.

### Working directory convention
Unless a step says otherwise, commands run from the repo root `C:/Users/SongMu/documents/claudecode/vba/bible`. Python imports inside the package assume `cwd=tools/aoc-mcp` only when running `python -m aoc_mcp.<module>` after the venv is active — the venv's `pip install -e .` step makes the package importable globally-in-venv, so module-run works from anywhere in the shell.

### Test running convention
```bash
source tools/aoc-mcp/.venv/Scripts/activate
pytest tools/aoc-mcp/tests/ -v
```

### Dependencies on interactive steps
Tasks 5, 6, and 14 require the user to log into AOC in a real browser or restart Claude Code. These are marked **INTERACTIVE**. The executing agent stops and waits for the user to complete the manual step before proceeding.

---

## Pre-Task setup: branch decision

This plan is additive-only to the existing `main` branch (touches only `tools/aoc-mcp/`, `.mcp.json` at repo root, `.gitignore` at repo root). No wiki content is affected. Default: work on `main`. If a feature branch is desired, switch before Task 1.

---

## Task 1: Scaffold `tools/aoc-mcp/` package

**Files:**
- Create: `tools/aoc-mcp/pyproject.toml`
- Create: `tools/aoc-mcp/.gitignore`
- Create: `tools/aoc-mcp/README.md`
- Create: `tools/aoc-mcp/aoc_mcp/__init__.py`
- Create: `tools/aoc-mcp/tests/__init__.py`
- Create: `tools/aoc-mcp/tests/fixtures/.gitkeep`

- [ ] **Step 1: Create directory tree**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
mkdir -p tools/aoc-mcp/aoc_mcp tools/aoc-mcp/tests/fixtures
```
Expected: no output, directories created.

- [ ] **Step 2: Write `tools/aoc-mcp/pyproject.toml`**

```toml
[project]
name = "aoc-mcp"
version = "0.1.0"
description = "MCP server for Art of Coaching Volleyball (paid-member access)"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.0.0",
    "playwright>=1.40",
    "httpx>=0.27",
    "beautifulsoup4>=4.12",
    "markdownify>=0.11",
    "pydantic>=2.5",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23"]

[project.scripts]
aoc-auth = "aoc_mcp.auth:main"

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["aoc_mcp*"]
```

- [ ] **Step 3: Write `tools/aoc-mcp/.gitignore`**

```
.venv/
__pycache__/
*.pyc
*.pyo
.session.json
.pytest_cache/
*.egg-info/
build/
dist/
```

- [ ] **Step 4: Write `tools/aoc-mcp/README.md` (initial stub; expanded in Task 15)**

```markdown
# AOC MCP

Local MCP server exposing Art of Coaching Volleyball (paid-member) content as tools for Claude Code and other MCP clients. Part of the Volleyball Coaching Bible wiki project.

See `docs/superpowers/specs/2026-04-23-aoc-mcp-design.md` (in the parent repo) for the full design.

## Install

```bash
cd tools/aoc-mcp
python -m venv .venv
source .venv/Scripts/activate        # Windows bash; see README for cmd/PowerShell
pip install -e .[dev]
playwright install chromium
```

## First-time auth

```bash
python -m aoc_mcp.auth
```

Opens Chromium. Log into AOC manually. On success, `.session.json` is saved and the window closes.

## More

Run `pytest` to verify install. See parent project's spec for detail.
```

- [ ] **Step 5: Write `tools/aoc-mcp/aoc_mcp/__init__.py`**

```python
"""AOC MCP — Art of Coaching Volleyball MCP server."""
__version__ = "0.1.0"
```

- [ ] **Step 6: Write `tools/aoc-mcp/tests/__init__.py`**

(empty file — marker for Python package)

```python
```

- [ ] **Step 7: Create fixtures folder marker**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
touch tools/aoc-mcp/tests/fixtures/.gitkeep
```

- [ ] **Step 8: Create venv and install deps**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
pip install -e ".[dev]"
```
Expected: pip successfully installs mcp, playwright, httpx, bs4, markdownify, pydantic, pytest, pytest-asyncio, and the editable `aoc-mcp` package.

- [ ] **Step 9: Install Playwright Chromium**

```bash
# still in venv from Step 8
playwright install chromium
```
Expected: Downloads ~200MB Chromium to `~/.cache/ms-playwright/chromium-*`. First run may take a minute.

- [ ] **Step 10: Smoke test — import the package**

```bash
python -c "import aoc_mcp; print(aoc_mcp.__version__)"
```
Expected: `0.1.0`

- [ ] **Step 11: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/pyproject.toml tools/aoc-mcp/.gitignore tools/aoc-mcp/README.md tools/aoc-mcp/aoc_mcp/__init__.py tools/aoc-mcp/tests/__init__.py tools/aoc-mcp/tests/fixtures/.gitkeep
git commit -m "chore: scaffold aoc-mcp package (Task 1)"
```

---

## Task 2: `config.py` — constants

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/config.py`

- [ ] **Step 1: Write `config.py`**

```python
"""Configuration constants for the AOC MCP server.

No logic — only constants. Anything that needs to be tuned goes here so other
modules don't hard-code magic values.
"""
from pathlib import Path

# AOC site
AOC_BASE_URL = "https://www.theartofcoachingvolleyball.com"
AOC_LOGIN_URL = f"{AOC_BASE_URL}/login"

# User-Agent: a recent Chrome UA. Update manually when it ages. Matching the UA
# used during headed login (Playwright-Chromium) reduces fingerprint mismatch.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Session storage (gitignored)
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SESSION_FILE = PACKAGE_ROOT / ".session.json"
FIXTURES_DIR = PACKAGE_ROOT / "tests" / "fixtures"

# HTTP behavior
DEFAULT_TIMEOUT_S = 30.0
REQUEST_MIN_INTERVAL_S = 1.0   # rate limit: min spacing between requests

# Auth timeout
AUTH_LOGIN_TIMEOUT_S = 300     # user has 5 minutes to log in manually

# Known topic slugs for aoc_list_recent (extended during discovery; see Task 6)
# Maps our slug → (display name, AOC category URL path).
KNOWN_TOPICS: dict[str, tuple[str, str]] = {
    # populated in Task 6 from live AOC inspection
}

# Session-cookie names to detect during Playwright login. Populated in Task 5.
AUTH_COOKIE_NAMES: list[str] = [
    # populated in Task 5 after observing the real login flow
]
```

- [ ] **Step 2: Smoke test — import constants**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
python -c "from aoc_mcp import config; print(config.AOC_BASE_URL, config.SESSION_FILE)"
```
Expected: prints `https://www.theartofcoachingvolleyball.com <absolute path>/.session.json`

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/config.py
git commit -m "feat: add config constants for aoc-mcp (Task 2)"
```

---

## Task 3: `errors.py` — structured error types

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/errors.py`
- Create: `tools/aoc-mcp/tests/test_errors.py`

- [ ] **Step 1: Write the failing test first**

`tools/aoc-mcp/tests/test_errors.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
pytest tests/test_errors.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'aoc_mcp.errors'`

- [ ] **Step 3: Implement `errors.py`**

```python
"""Structured error types for the AOC MCP server.

All errors inherit from AocError so the MCP server boundary can catch them
with a single handler and convert to structured MCP error responses.
"""


class AocError(Exception):
    """Base class for all AOC MCP errors."""

    code: str = "aoc_error"


class SessionExpired(AocError):
    """The saved AOC session is missing or has expired."""

    code = "session_expired"

    def __init__(self, message: str | None = None):
        super().__init__(
            message
            or "AOC session expired. Re-authenticate: run "
            "`python -m aoc_mcp.auth` from tools/aoc-mcp/"
        )


class NotFound(AocError):
    """The requested AOC URL returned 404."""

    code = "not_found"

    def __init__(self, url: str):
        self.url = url
        super().__init__(f"{url} returned 404")


class RateLimited(AocError):
    """AOC returned 429 after retry exhausted."""

    code = "rate_limited"

    def __init__(self, url: str):
        self.url = url
        super().__init__(f"{url} rate-limited (429) after retry")


class UpstreamError(AocError):
    """AOC returned 5xx after retry exhausted."""

    code = "upstream_error"

    def __init__(self, url: str, status: int):
        self.url = url
        self.status = status
        super().__init__(f"{url} upstream error ({status}) after retry")


class ParserFailed(AocError):
    """Could not extract the expected structure from a fetched page."""

    code = "parser_failed"

    def __init__(self, url: str, snippet: str):
        self.url = url
        # cap snippet to keep MCP error payload small
        self.snippet = snippet[:500]
        super().__init__(
            f"Parser failed for {url}. First 500 chars of HTML: {self.snippet!r}"
        )


class UnsupportedProvider(AocError):
    """Video page uses an embed provider we don't support."""

    code = "unsupported_provider"

    def __init__(self, url: str, provider: str):
        self.url = url
        self.provider = provider
        super().__init__(f"{url} uses unsupported provider: {provider}")


class UnknownTopic(AocError):
    """The topic slug passed to aoc_list_recent is not in our known list."""

    code = "unknown_topic"

    def __init__(self, topic: str, known_topics: list[str]):
        self.topic = topic
        self.known_topics = known_topics
        super().__init__(
            f"Unknown topic '{topic}'. Known: {', '.join(sorted(known_topics))}"
        )
```

- [ ] **Step 4: Run tests to verify pass**

```bash
pytest tests/test_errors.py -v
```
Expected: PASS (5 tests green).

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/errors.py tools/aoc-mcp/tests/test_errors.py
git commit -m "feat: structured error hierarchy for aoc-mcp (Task 3)"
```

---

## Task 4: `client.py` — AocClient with session-expiry sniff

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/client.py`
- Create: `tools/aoc-mcp/tests/test_client.py`
- Create: `tools/aoc-mcp/tests/fixtures/login-redirect-response.html`
- Create: `tools/aoc-mcp/tests/fixtures/authenticated-article-response.html`

Test fixtures are hand-fabricated minimal HTML here — not real AOC captures yet. Real fixtures come in Task 6.

- [ ] **Step 1: Write synthetic fixtures for session-expiry testing**

`tools/aoc-mcp/tests/fixtures/login-redirect-response.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Log In - Art of Coaching Volleyball</title></head>
<body>
<form id="loginform" action="https://www.theartofcoachingvolleyball.com/wp-login.php" method="post">
<input name="log" type="text" />
<input name="pwd" type="password" />
<button type="submit">Log In</button>
</form>
</body>
</html>
```

`tools/aoc-mcp/tests/fixtures/authenticated-article-response.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Sample AOC Article - Art of Coaching Volleyball</title></head>
<body>
<article class="post">
<h1 class="entry-title">Sample Article Title</h1>
<div class="entry-content">
<p>Paragraph one of the article body.</p>
</div>
</article>
</body>
</html>
```

- [ ] **Step 2: Write the failing tests**

`tools/aoc-mcp/tests/test_client.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
pytest tests/test_client.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'aoc_mcp.client'`.

- [ ] **Step 4: Implement `client.py`**

```python
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
        elapsed = time.monotonic() - self._last_request_time
        min_interval = config.REQUEST_MIN_INTERVAL_S
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

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
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_client.py -v
```
Expected: PASS (6 tests green).

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/client.py tools/aoc-mcp/tests/test_client.py tools/aoc-mcp/tests/fixtures/login-redirect-response.html tools/aoc-mcp/tests/fixtures/authenticated-article-response.html
git commit -m "feat: AocClient with session-expiry sniff + rate limiting (Task 4)"
```

---

## Task 5: `auth.py` — Playwright headed login CLI (**INTERACTIVE**)

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/auth.py`

No automated tests for this module — it's a Playwright wrapper that requires a real browser + real credentials. A manual smoke test is performed at the end (checkpoint IC1).

- [ ] **Step 1: Write `auth.py`**

```python
"""Playwright headed-login CLI for AOC.

Usage:
    python -m aoc_mcp.auth           # login mode: opens headed Chromium
    python -m aoc_mcp.auth --verify  # checks if existing session is valid
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

from aoc_mcp import config


async def run_login() -> int:
    """Open headed Chromium, wait for the user to log in, save session state."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=config.USER_AGENT)
        page = await context.new_page()

        print(f"[auth] Opening {config.AOC_LOGIN_URL} ...")
        await page.goto(config.AOC_LOGIN_URL)
        print(
            f"[auth] Please log into AOC in the opened browser window.\n"
            f"[auth] You have {config.AUTH_LOGIN_TIMEOUT_S // 60} minutes.\n"
            f"[auth] Waiting for login-completion signal..."
        )

        deadline = time.monotonic() + config.AUTH_LOGIN_TIMEOUT_S
        logged_in = False
        while time.monotonic() < deadline:
            await asyncio.sleep(2.0)
            cookies = await context.cookies()
            # Primary signal: cookie with name starting "wordpress_logged_in_"
            # (WordPress convention) OR any cookie matching the configured list.
            for c in cookies:
                name = c.get("name", "")
                if name.startswith("wordpress_logged_in_") or (
                    config.AUTH_COOKIE_NAMES
                    and name in config.AUTH_COOKIE_NAMES
                ):
                    logged_in = True
                    break
            if logged_in:
                break

        if not logged_in:
            print("[auth] ERROR: login timeout — no auth cookie observed.", file=sys.stderr)
            await browser.close()
            return 1

        config.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(config.SESSION_FILE))
        print(f"[auth] Authenticated. Session saved to {config.SESSION_FILE}")
        await browser.close()
        return 0


async def run_verify() -> int:
    """Load the saved session, hit a minimal AOC URL, check for login-form signal."""
    from aoc_mcp.client import AocClient
    from aoc_mcp.errors import SessionExpired, AocError

    try:
        client = AocClient()
    except SessionExpired:
        print("[auth] Session file missing or malformed.", file=sys.stderr)
        return 1

    try:
        client.get(config.AOC_BASE_URL)
    except SessionExpired:
        print("[auth] Session is EXPIRED. Run `python -m aoc_mcp.auth` to re-auth.")
        return 1
    except AocError as e:
        print(f"[auth] Unexpected error during verify: {e}", file=sys.stderr)
        return 2

    print("[auth] Session is VALID.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="AOC auth CLI")
    parser.add_argument("--verify", action="store_true",
                        help="Only verify existing session; do not log in")
    args = parser.parse_args()
    coro = run_verify() if args.verify else run_login()
    return asyncio.run(coro)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Static sanity check — imports and CLI help work**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
python -m aoc_mcp.auth --help
```
Expected: argparse usage message for `--verify`.

- [ ] **Step 3: Commit the code (pre-smoke-test)**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/auth.py
git commit -m "feat: Playwright headed-login auth CLI (Task 5)"
```

- [ ] **Step 4 (INTERACTIVE — IC1): User runs live auth**

The user executes:
```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
python -m aoc_mcp.auth
```

A Chromium window opens at AOC's login page. User logs in. The terminal prints:
- `[auth] Opening https://.../login ...`
- `[auth] Please log into AOC in the opened browser window...`
- After login: `[auth] Authenticated. Session saved to .../.session.json`

If login detection fails (timeout), the user reports the cookie names they can see in DevTools → Application → Cookies. The agent updates `config.AUTH_COOKIE_NAMES` with the observed cookie name(s), re-commits config, and re-runs from Step 4.

- [ ] **Step 5 (INTERACTIVE — IC1 verify): User confirms session is saved**

```bash
ls -la tools/aoc-mcp/.session.json
python -m aoc_mcp.auth --verify
```
Expected: `.session.json` exists, non-empty; `--verify` prints `[auth] Session is VALID.`

If `AUTH_COOKIE_NAMES` was updated in the previous step, commit that change:
```bash
git add tools/aoc-mcp/aoc_mcp/config.py
git commit -m "chore: capture observed AOC auth cookie names (Task 5)"
```

---

## Task 6: `discover.py` — capture live AOC fixtures (**INTERACTIVE**)

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/discover.py`

This subcommand uses the saved session to fetch target AOC URLs and save their HTML to `tests/fixtures/` so Tasks 7–10 can TDD against real pages.

- [ ] **Step 1: Write `discover.py`**

```python
"""Fetch live AOC pages and save as test fixtures.

Usage:
    python -m aoc_mcp.discover               # fetches the default seed set
    python -m aoc_mcp.discover <url> <slug>  # fetch one URL, save as <slug>.html

The default seed set covers the page types the extractors need to handle:
- 1 article (ideally a Premium one to verify auth works)
- 1 search results page
- 1 topic category page
- 1 video page
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aoc_mcp import config
from aoc_mcp.client import AocClient

# Default seed: (slug, url). Update these as understanding of AOC improves.
# Slug becomes the filename under tests/fixtures/: <slug>.html
DEFAULT_SEEDS: list[tuple[str, str]] = [
    (
        "live-article-kiraly-4-keys-forearm-pass",
        "https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/",
    ),
    (
        "live-search-karch",
        "https://www.theartofcoachingvolleyball.com/?s=karch",
    ),
    (
        "live-category-passing",
        "https://www.theartofcoachingvolleyball.com/category/passing/",
    ),
    # Video seed added after user confirms a specific video URL; see Task 6 Step 4.
]


def save_fixture(slug: str, url: str) -> Path:
    out = config.FIXTURES_DIR / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    with AocClient() as client:
        response = client.get(url)

    out.write_text(response.text, encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"[discover] Saved {out.name} ({size_kb:.1f} KB)")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Save AOC fixtures")
    parser.add_argument("url", nargs="?", default=None)
    parser.add_argument("slug", nargs="?", default=None)
    args = parser.parse_args()

    if args.url and args.slug:
        try:
            save_fixture(args.slug, args.url)
        except Exception as e:
            print(f"[discover] ERROR saving {args.slug}: {e}", file=sys.stderr)
            return 1
        return 0

    exit_code = 0
    for slug, url in DEFAULT_SEEDS:
        try:
            save_fixture(slug, url)
        except Exception as e:
            print(f"[discover] ERROR on {slug}: {e}", file=sys.stderr)
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Commit `discover.py`**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/discover.py
git commit -m "feat: discover.py for capturing live AOC fixtures (Task 6)"
```

- [ ] **Step 3 (INTERACTIVE — IC2): User runs discover with default seeds**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
python -m aoc_mcp.discover
```
Expected: 3 `.html` files appear in `tests/fixtures/` (`live-article-kiraly-4-keys-forearm-pass.html`, `live-search-karch.html`, `live-category-passing.html`). If the article fetch hits a paywall sniff (content too thin), check `--verify` — session may have expired between Tasks 5 and 6.

- [ ] **Step 4 (INTERACTIVE — IC2): User identifies a video URL and captures it**

User picks one AOC video page URL (ideally Premium) and runs:
```bash
python -m aoc_mcp.discover "<aoc video page url>" "live-video-sample"
```
Expected: `live-video-sample.html` in `tests/fixtures/`.

- [ ] **Step 5: Inspect fixtures and populate `config.KNOWN_TOPICS`**

Open `tests/fixtures/live-category-passing.html` and identify the URL pattern for topics (likely `/category/<slug>/`). Populate `aoc_mcp/config.py`:

```python
KNOWN_TOPICS: dict[str, tuple[str, str]] = {
    "passing":           ("Passing",           "/category/passing/"),
    "setting":           ("Setting",           "/category/setting/"),
    "hitting":           ("Hitting",           "/category/hitting/"),
    "blocking":          ("Blocking",          "/category/blocking/"),
    "serving":           ("Serving",           "/category/serving/"),
    "defense":           ("Defense",           "/category/defense/"),
    "practice-planning": ("Practice Planning", "/category/practice-planning/"),
    "season-planning":   ("Season Planning",   "/category/season-planning/"),
    "mental":            ("Mental Game",       "/category/mental-game/"),
    "recruiting":        ("Recruiting",        "/category/recruiting/"),
}
```

Adjust slugs + paths based on what the category page shows AOC actually uses (e.g., `/mental-game/` vs `/mental/`). The values are `(display_name, url_path)`.

- [ ] **Step 6: Commit fixtures + config update**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/tests/fixtures/live-*.html tools/aoc-mcp/aoc_mcp/config.py
git commit -m "chore: capture live AOC fixtures + populate KNOWN_TOPICS (Task 6)"
```

---

## Task 7: `extract.py` — article HTML → markdown (TDD against live fixture)

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/extract.py`
- Create: `tools/aoc-mcp/aoc_mcp/models.py`
- Create: `tools/aoc-mcp/tests/test_extract.py`

- [ ] **Step 1: Write `models.py` with shared pydantic types**

`tools/aoc-mcp/aoc_mcp/models.py`:

```python
"""Shared pydantic models for MCP tool return values."""
from pydantic import BaseModel, Field


class ArticleResult(BaseModel):
    title: str
    author: str | None = None
    date: str | None = None       # ISO-8601 YYYY-MM-DD if parseable, else None
    tags: list[str] = Field(default_factory=list)
    markdown: str
    word_count: int
    url: str


class SearchHit(BaseModel):
    title: str
    url: str
    author: str | None = None
    snippet: str = ""
    date: str | None = None


class SearchResult(BaseModel):
    hits: list[SearchHit]
    total_returned: int


class VideoResult(BaseModel):
    title: str
    author: str | None = None
    duration_sec: int | None = None
    transcript: str | None = None
    captions_source: str = "unavailable"  # vimeo|wistia|unavailable|unsupported_provider
    embed_url: str | None = None
    url: str
```

- [ ] **Step 2: Inspect the live article fixture and note the DOM structure**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
grep -o '<h1[^>]*class="[^"]*"' tests/fixtures/live-article-kiraly-4-keys-forearm-pass.html | head -5
grep -oE 'class="(entry-title|entry-content|entry-meta|post-author|entry-date)[^"]*"' tests/fixtures/live-article-kiraly-4-keys-forearm-pass.html | head -20
grep -oE '<meta[^>]*property="article:published_time"[^>]*>' tests/fixtures/live-article-kiraly-4-keys-forearm-pass.html | head -1
```
The output tells you which selectors to use. **Task Step 3's code uses placeholder selectors** (`.entry-title`, `.entry-content`, `.entry-meta`, etc. — WordPress defaults) that are likely right for AOC, but you MUST confirm against the live fixture. If AOC uses different classes, update the selector constants at the top of `extract.py`.

- [ ] **Step 3: Write the failing tests**

`tools/aoc-mcp/tests/test_extract.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they fail**

```bash
pytest tests/test_extract.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'aoc_mcp.extract'`.

- [ ] **Step 5: Implement `extract.py`**

```python
"""Parse AOC article HTML into ArticleResult.

Selectors are captured from live AOC fixtures. If AOC updates its theme/DOM,
update these SELECTORS constants and re-run extract tests.
"""
from __future__ import annotations

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from aoc_mcp.errors import ParserFailed
from aoc_mcp.models import ArticleResult

# WordPress defaults — confirmed against live fixture in Task 6.
# If AOC changes themes, update these.
SELECTOR_TITLE = "h1.entry-title"
SELECTOR_BODY = "div.entry-content, article .entry-content"
SELECTOR_AUTHOR = ".author.vcard a, .byline .author, .entry-meta .author"
SELECTOR_DATE_META = 'meta[property="article:published_time"]'
SELECTOR_TAGS = ".entry-categories a, .entry-tags a, .cat-links a"

# Tags/attributes to strip aggressively from the body before md conversion
STRIP_SELECTORS = [
    "script",
    "style",
    "nav",
    "header",
    "footer",
    "aside",
    ".site-header",
    ".site-footer",
    ".menu-primary",
    ".sharedaddy",         # Jetpack share buttons
    ".jp-relatedposts",    # Jetpack related posts
    ".author-box",
    ".post-navigation",
    ".comments-area",
    "form",
]


def parse_article(html: str, *, url: str) -> ArticleResult:
    """Parse AOC article HTML. Raises ParserFailed if critical selectors miss."""
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one(SELECTOR_TITLE)
    body_el = soup.select_one(SELECTOR_BODY)

    if not title_el or not body_el:
        raise ParserFailed(url=url, snippet=html[:500])

    title = title_el.get_text(strip=True)

    # Strip chrome from body before md conversion.
    for sel in STRIP_SELECTORS:
        for junk in body_el.select(sel):
            junk.decompose()

    body_html = str(body_el)
    markdown_text = md(body_html, heading_style="ATX").strip()

    # Remove excessive blank lines (markdownify often leaves 3+ consecutive newlines).
    lines: list[str] = []
    blank_run = 0
    for line in markdown_text.splitlines():
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                lines.append("")
        else:
            blank_run = 0
            lines.append(line)
    markdown_text = "\n".join(lines).strip()

    word_count = len(markdown_text.split())

    author_el = soup.select_one(SELECTOR_AUTHOR)
    author = author_el.get_text(strip=True) if author_el else None

    date_meta = soup.select_one(SELECTOR_DATE_META)
    date = None
    if date_meta and date_meta.get("content"):
        date = date_meta["content"][:10]  # ISO date prefix

    tag_els = soup.select(SELECTOR_TAGS)
    tags = [t.get_text(strip=True) for t in tag_els if t.get_text(strip=True)]

    return ArticleResult(
        title=title,
        author=author,
        date=date,
        tags=tags,
        markdown=markdown_text,
        word_count=word_count,
        url=url,
    )
```

- [ ] **Step 6: Run tests; iterate selectors until pass**

```bash
pytest tests/test_extract.py -v
```
If a test fails because the title selector missed (common if AOC uses a non-default theme), inspect the live fixture:
```bash
grep -E 'class="[^"]*title[^"]*"' tests/fixtures/live-article-kiraly-4-keys-forearm-pass.html | head -10
```
Update `SELECTOR_TITLE` (or whichever selector is off) and re-run. Repeat until all 5 tests green.

Expected (final): PASS (5 tests).

- [ ] **Step 7: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/models.py tools/aoc-mcp/aoc_mcp/extract.py tools/aoc-mcp/tests/test_extract.py
git commit -m "feat: parse AOC article HTML into ArticleResult (Task 7)"
```

---

## Task 8: `search.py` — AOC search results parser

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/search.py`
- Create: `tools/aoc-mcp/tests/test_search.py`

- [ ] **Step 1: Inspect the live search fixture**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
grep -oE 'class="[^"]*(search-result|post|entry)[^"]*"' tests/fixtures/live-search-karch.html | sort -u | head -20
```
Identify the repeating-item selector (e.g., `article.post`, `.search-result`, `.hentry`). Use it in `SELECTOR_RESULT_ITEM` below.

- [ ] **Step 2: Write failing tests**

`tools/aoc-mcp/tests/test_search.py`:

```python
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
```

- [ ] **Step 3: Run tests — verify they fail**

```bash
pytest tests/test_search.py -v
```
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 4: Implement `search.py`**

```python
"""Parse AOC search-results HTML into SearchResult."""
from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from aoc_mcp import config
from aoc_mcp.client import AocClient
from aoc_mcp.models import SearchHit, SearchResult

# WordPress defaults; confirm against live-search fixture in Task 8 Step 1.
SELECTOR_RESULT_ITEM = "article.post, article.hentry, .search-result"
SELECTOR_ITEM_TITLE = "h2 a, h3 a, .entry-title a"
SELECTOR_ITEM_SNIPPET = ".entry-summary, .entry-content p, .post-excerpt"
SELECTOR_ITEM_AUTHOR = ".author.vcard a, .byline .author"
SELECTOR_ITEM_DATE = ".entry-date, time.published"


def parse_search_results(html: str, *, limit: int = 10) -> SearchResult:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(SELECTOR_RESULT_ITEM)
    hits: list[SearchHit] = []
    for item in items[:limit]:
        title_el = item.select_one(SELECTOR_ITEM_TITLE)
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        url = title_el.get("href", "")
        if not url:
            continue
        url = urljoin(config.AOC_BASE_URL, url)

        snippet_el = item.select_one(SELECTOR_ITEM_SNIPPET)
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "…"

        author_el = item.select_one(SELECTOR_ITEM_AUTHOR)
        author = author_el.get_text(strip=True) if author_el else None

        date_el = item.select_one(SELECTOR_ITEM_DATE)
        date = None
        if date_el:
            iso = date_el.get("datetime")
            if iso:
                date = iso[:10]
            else:
                date = date_el.get_text(strip=True)

        hits.append(SearchHit(
            title=title, url=url, author=author, snippet=snippet, date=date
        ))
    return SearchResult(hits=hits, total_returned=len(hits))


def run_search(query: str, *, limit: int = 10) -> SearchResult:
    """Execute a live AOC search via AocClient."""
    from urllib.parse import urlencode
    search_url = f"{config.AOC_BASE_URL}/?" + urlencode({"s": query})
    with AocClient() as client:
        response = client.get(search_url)
    return parse_search_results(response.text, limit=limit)
```

- [ ] **Step 5: Run tests; iterate selectors until pass**

```bash
pytest tests/test_search.py -v
```
If items aren't found, adjust `SELECTOR_RESULT_ITEM` based on Step 1's inspection. Rerun.

Expected: PASS (4 tests).

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/search.py tools/aoc-mcp/tests/test_search.py
git commit -m "feat: AOC search results parser (Task 8)"
```

---

## Task 9: `catalog.py` — topic/category listing

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/catalog.py`
- Create: `tools/aoc-mcp/tests/test_catalog.py`

- [ ] **Step 1: Write failing tests**

`tools/aoc-mcp/tests/test_catalog.py`:

```python
"""Tests for aoc_mcp.catalog — topic listing."""
from pathlib import Path

import pytest

from aoc_mcp.catalog import parse_category_page
from aoc_mcp.errors import UnknownTopic

FIXTURES = Path(__file__).parent / "fixtures"
LIVE_CATEGORY = FIXTURES / "live-category-passing.html"


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
```

- [ ] **Step 2: Run tests — verify fail**

```bash
pytest tests/test_catalog.py -v
```
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement `catalog.py`**

```python
"""AOC category/topic listing."""
from __future__ import annotations

from aoc_mcp import config
from aoc_mcp.client import AocClient
from aoc_mcp.errors import UnknownTopic
from aoc_mcp.models import SearchResult
from aoc_mcp.search import parse_search_results

# Category pages on WordPress use the same post-list DOM as search pages,
# so we reuse parse_search_results for the parse step.
parse_category_page = parse_search_results


def list_recent(topic: str, *, limit: int = 20) -> SearchResult:
    """Fetch the most recent N items in an AOC topic category."""
    if topic not in config.KNOWN_TOPICS:
        raise UnknownTopic(topic=topic, known_topics=list(config.KNOWN_TOPICS.keys()))
    _, path = config.KNOWN_TOPICS[topic]
    url = config.AOC_BASE_URL + path
    with AocClient() as client:
        response = client.get(url)
    return parse_category_page(response.text, limit=limit)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_catalog.py -v
```
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/catalog.py tools/aoc-mcp/tests/test_catalog.py
git commit -m "feat: AOC topic catalog listing (Task 9)"
```

---

## Task 10: `video.py` — video transcript via Playwright + provider captions

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/video.py`

This module uses Playwright in headless mode (unlike auth.py which is headed) to load JS-heavy video pages and extract the embed URL. Provider-specific caption fetch uses the embed URL to build a captions request. Testing is manual — no fixture test beyond the embed-URL-extraction regex, since caption endpoints require a live provider response.

- [ ] **Step 1: Inspect the video fixture for embed pattern**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
grep -oE 'player\.vimeo\.com/video/[0-9]+' tests/fixtures/live-video-sample.html | head -3
grep -oE 'fast\.wistia\.(net|com)/embed/iframe/[a-z0-9]+' tests/fixtures/live-video-sample.html | head -3
```
Confirms which provider AOC uses. Hopefully Vimeo for the test sample.

- [ ] **Step 2: Write `video.py`**

```python
"""Extract video transcripts from AOC video pages.

Flow:
  1. Load the AOC page in headless Playwright (JS renders the iframe).
  2. Extract the embedded Vimeo/Wistia URL.
  3. For Vimeo: call the player config to get the caption URLs, fetch VTT.
  4. For Wistia: fetch the caption JSON.
  5. Assemble VideoResult.
"""
from __future__ import annotations

import asyncio
import json
import re
from typing import Optional

import httpx
from playwright.async_api import async_playwright

from aoc_mcp import config
from aoc_mcp.errors import ParserFailed, SessionExpired, UnsupportedProvider
from aoc_mcp.models import VideoResult

VIMEO_RE = re.compile(r"player\.vimeo\.com/video/(\d+)")
WISTIA_RE = re.compile(r"fast\.wistia\.(?:net|com)/embed/(?:iframe|medias)/([a-z0-9]+)")


async def _extract_embed_from_page(page_url: str) -> tuple[str | None, str, str | None]:
    """Return (embed_url, title, author_or_none) from an AOC video page.

    Uses headless Playwright so JS-rendered iframes are visible. Loads the saved
    AOC session cookies so Premium video pages render correctly.
    """
    if not config.SESSION_FILE.exists():
        raise SessionExpired()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(config.SESSION_FILE),
            user_agent=config.USER_AGENT,
        )
        page = await context.new_page()
        await page.goto(page_url, wait_until="networkidle", timeout=60_000)

        # Title
        title = await page.title()
        # Strip " - Art of Coaching Volleyball" suffix if present
        title = re.sub(r"\s*[-|]\s*Art of Coaching Volleyball\s*$", "", title)

        # Try common author selectors
        author: str | None = None
        for sel in [".author.vcard a", ".byline .author", ".entry-meta .author"]:
            el = await page.query_selector(sel)
            if el:
                author = (await el.text_content() or "").strip() or None
                break

        # Extract embed URL from iframe src
        iframes = await page.query_selector_all("iframe")
        embed_url: str | None = None
        for ifr in iframes:
            src = await ifr.get_attribute("src") or ""
            if "vimeo.com" in src or "wistia" in src:
                embed_url = src
                break

        await browser.close()
        return embed_url, title, author


def _detect_provider(embed_url: str) -> tuple[str, str] | None:
    """Return (provider_name, provider_id) or None."""
    if m := VIMEO_RE.search(embed_url):
        return "vimeo", m.group(1)
    if m := WISTIA_RE.search(embed_url):
        return "wistia", m.group(1)
    return None


async def _fetch_vimeo_captions(video_id: str) -> Optional[str]:
    """Try to fetch Vimeo captions via the public config API.

    Vimeo exposes video configs at https://player.vimeo.com/video/<id>/config.
    The config JSON may include `request.text_tracks` with caption URLs.
    This endpoint may require a Referer header matching AOC or a token — if
    it returns 403, we fall back to returning None.
    """
    config_url = f"https://player.vimeo.com/video/{video_id}/config"
    async with httpx.AsyncClient(
        timeout=config.DEFAULT_TIMEOUT_S,
        headers={
            "User-Agent": config.USER_AGENT,
            "Referer": config.AOC_BASE_URL,
        },
    ) as hc:
        try:
            r = await hc.get(config_url)
            r.raise_for_status()
            data = r.json()
        except (httpx.HTTPError, json.JSONDecodeError):
            return None

        tracks = data.get("request", {}).get("text_tracks", [])
        if not tracks:
            return None

        # Prefer English auto-captions if present, else first track
        en = next((t for t in tracks if t.get("lang", "").startswith("en")), None)
        track = en or tracks[0]
        track_url = track.get("url")
        if not track_url:
            return None
        if track_url.startswith("/"):
            track_url = "https://player.vimeo.com" + track_url

        try:
            r = await hc.get(track_url)
            r.raise_for_status()
            vtt_body = r.text
        except httpx.HTTPError:
            return None

    return _vtt_to_plain_text(vtt_body)


def _vtt_to_plain_text(vtt: str) -> str:
    """Strip WEBVTT headers + cue timings, join cue text."""
    lines: list[str] = []
    for line in vtt.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("WEBVTT"):
            continue
        if "-->" in s:
            continue
        if s.isdigit():  # cue number
            continue
        lines.append(s)
    return "\n".join(lines).strip()


async def _get_transcript_async(url: str) -> VideoResult:
    embed_url, title, author = await _extract_embed_from_page(url)
    if not embed_url:
        return VideoResult(
            title=title, author=author, transcript=None,
            captions_source="unavailable", embed_url=None, url=url,
        )

    provider = _detect_provider(embed_url)
    if not provider:
        return VideoResult(
            title=title, author=author, transcript=None,
            captions_source="unsupported_provider", embed_url=embed_url, url=url,
        )

    provider_name, provider_id = provider
    if provider_name == "vimeo":
        transcript = await _fetch_vimeo_captions(provider_id)
        return VideoResult(
            title=title, author=author, transcript=transcript,
            captions_source="vimeo" if transcript else "unavailable",
            embed_url=embed_url, url=url,
        )

    # Wistia: left as a future extension; returns unsupported for now.
    return VideoResult(
        title=title, author=author, transcript=None,
        captions_source="unsupported_provider", embed_url=embed_url, url=url,
    )


def get_transcript(url: str) -> VideoResult:
    """Sync entry point (MCP tool handlers call this)."""
    return asyncio.run(_get_transcript_async(url))
```

- [ ] **Step 3: Quick unit test for provider detection**

Append to `tools/aoc-mcp/tests/test_client.py` (same file — small helper) OR create a focused test file. Creating a new one for clarity:

`tools/aoc-mcp/tests/test_video.py`:
```python
"""Unit tests for aoc_mcp.video helper functions."""
from aoc_mcp.video import _detect_provider, _vtt_to_plain_text


def test_detect_provider_vimeo():
    assert _detect_provider("https://player.vimeo.com/video/123456789?autoplay=1") == (
        "vimeo", "123456789"
    )


def test_detect_provider_wistia():
    assert _detect_provider("https://fast.wistia.net/embed/iframe/abcd1234") == (
        "wistia", "abcd1234"
    )


def test_detect_provider_unknown():
    assert _detect_provider("https://youtube.com/embed/xyz") is None


def test_vtt_to_plain_text_strips_timings_and_headers():
    vtt = (
        "WEBVTT\n\n"
        "1\n00:00:00.000 --> 00:00:02.500\nHello world\n\n"
        "2\n00:00:02.500 --> 00:00:05.000\nSecond cue\n"
    )
    assert _vtt_to_plain_text(vtt) == "Hello world\nSecond cue"
```

- [ ] **Step 4: Run tests**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
pytest tests/test_video.py -v
```
Expected: PASS (4 tests).

- [ ] **Step 5: Manual smoke test — live video**

```bash
python -c "from aoc_mcp.video import get_transcript; import json; r = get_transcript('<the AOC video URL captured in Task 6 Step 4>'); print(json.dumps(r.model_dump(), indent=2)[:800])"
```
Expected output (sample shape, actual values vary):
```
{
  "title": "<video title>",
  "author": "<author or null>",
  "duration_sec": null,
  "transcript": "<VTT-stripped plain text if captions available, else null>",
  "captions_source": "vimeo" or "unavailable" or "unsupported_provider",
  "embed_url": "https://player.vimeo.com/video/...",
  ...
}
```
If `transcript` is null and `captions_source` is `unavailable`, that's expected for videos without captions — it's not a failure. If Playwright errors (e.g., timeout loading page), verify the session is still fresh (`python -m aoc_mcp.auth --verify`).

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/video.py tools/aoc-mcp/tests/test_video.py
git commit -m "feat: video transcript extraction via Playwright + Vimeo/Wistia (Task 10)"
```

---

## Task 11: `server.py` — MCP bootstrap, register 4 tools

**Files:**
- Create: `tools/aoc-mcp/aoc_mcp/server.py`

- [ ] **Step 1: Write `server.py`**

```python
"""MCP server entry point — stdio transport, registers 4 tools."""
from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from aoc_mcp import catalog, extract, search, video
from aoc_mcp.client import AocClient
from aoc_mcp.errors import AocError

server = Server("aoc-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="aoc_fetch_article",
            description=(
                "Fetch an AOC article URL (using the signed-in session) and "
                "return title, author, date, tags, markdown body, and word count."
            ),
            inputSchema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        ),
        Tool(
            name="aoc_search",
            description=(
                "Run a search against AOC's catalog and return matching articles/videos."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="aoc_list_recent",
            description=(
                "List recent items in an AOC topic (e.g., 'passing', 'setting'). "
                "Returns the most recent N articles."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="aoc_video_transcript",
            description=(
                "Fetch an AOC video page's transcript if captions are available "
                "on the underlying provider (Vimeo/Wistia)."
            ),
            inputSchema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        ),
    ]


def _error_payload(err: AocError) -> dict[str, Any]:
    payload = {"code": err.code, "message": str(err)}
    for attr in ("url", "snippet", "topic", "known_topics", "provider", "status"):
        if hasattr(err, attr):
            payload[attr] = getattr(err, attr)
    return payload


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    import json

    try:
        if name == "aoc_fetch_article":
            url = arguments["url"]
            with AocClient() as client:
                response = client.get(url)
            result = extract.parse_article(response.text, url=url).model_dump()
        elif name == "aoc_search":
            query = arguments["query"]
            limit = int(arguments.get("limit", 10))
            result = search.run_search(query, limit=limit).model_dump()
        elif name == "aoc_list_recent":
            topic = arguments["topic"]
            limit = int(arguments.get("limit", 20))
            result = catalog.list_recent(topic, limit=limit).model_dump()
        elif name == "aoc_video_transcript":
            url = arguments["url"]
            result = video.get_transcript(url).model_dump()
        else:
            result = {"code": "unknown_tool", "name": name}
    except AocError as e:
        result = _error_payload(e)
    except Exception as e:
        result = {
            "code": "runtime_error",
            "message": f"{type(e).__name__}: {e}",
        }
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def amain() -> int:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())
    return 0


def main() -> int:
    return asyncio.run(amain())


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Static sanity check**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
python -c "from aoc_mcp import server; print('ok', server.server.name)"
```
Expected: `ok aoc-mcp`

- [ ] **Step 3: Verify the tool registry compiles cleanly**

```bash
python -c "import asyncio; from aoc_mcp.server import list_tools; tools = asyncio.run(list_tools()); print([t.name for t in tools])"
```
Expected: `['aoc_fetch_article', 'aoc_search', 'aoc_list_recent', 'aoc_video_transcript']`. The Step 2 smoke check confirmed the module imports; this confirms the `@server.list_tools()` decorator is wired and the 4 tool schemas are well-formed.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/aoc_mcp/server.py
git commit -m "feat: MCP stdio server with 4 tools (Task 11)"
```

---

## Task 12: Register the MCP via `.mcp.json`

**Files:**
- Create: `.mcp.json` (at repo root)

- [ ] **Step 1: Write `.mcp.json`**

`C:/Users/SongMu/documents/claudecode/vba/bible/.mcp.json`:
```json
{
  "mcpServers": {
    "aoc": {
      "command": "tools/aoc-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "aoc_mcp.server"]
    }
  }
}
```

(If the user's primary development machine is not Windows, change the `command` path to `tools/aoc-mcp/.venv/bin/python`.)

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add .mcp.json
git commit -m "chore: register aoc-mcp server via .mcp.json (Task 12)"
```

---

## Task 13: Final README — install, auth, smoke test, troubleshooting

**Files:**
- Modify: `tools/aoc-mcp/README.md`

- [ ] **Step 1: Rewrite README**

```markdown
# AOC MCP

Local MCP server exposing Art of Coaching Volleyball (paid-member) content as tools for Claude Code and other MCP clients. Part of the Volleyball Coaching Bible wiki project.

## What it does

Four MCP tools:

- `aoc_fetch_article(url)` — fetch an article URL, return title/author/date/tags/markdown/word-count
- `aoc_search(query, limit=10)` — search the AOC catalog
- `aoc_list_recent(topic, limit=20)` — list recent items in a topic (`passing`, `setting`, etc.)
- `aoc_video_transcript(url)` — extract the transcript of a video page (Vimeo/Wistia captions)

## Install

Requires Python 3.11+. Disk: ~250MB (~200MB of that is Chromium).

```bash
cd tools/aoc-mcp
python -m venv .venv
source .venv/Scripts/activate         # Windows bash
# or: .venv\Scripts\activate          # Windows cmd/PowerShell
# or: source .venv/bin/activate       # macOS/Linux
pip install --upgrade pip
pip install -e ".[dev]"
playwright install chromium
```

## Auth

One-time per session lifetime (AOC cookies typically last 30–90 days):

```bash
python -m aoc_mcp.auth
```

A Chromium window opens at AOC's login page. Log in normally (handles MFA/captcha because it's a real browser). When the auth cookie is detected, the window closes and `.session.json` is saved.

Verify at any time:

```bash
python -m aoc_mcp.auth --verify
```

If this prints `Session is EXPIRED`, re-run `python -m aoc_mcp.auth`.

## Smoke test

```bash
pytest tests/ -v                                   # fixture-based unit tests

# Live-session tests (require auth from previous step):
python -m aoc_mcp.discover                         # refreshes fixtures
python -c "from aoc_mcp.extract import parse_article; from aoc_mcp.client import AocClient; \
import json; c = AocClient(); r = c.get('https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/'); \
print(parse_article(r.text, url=r.url.__str__()).model_dump_json(indent=2)[:500])"
```

## Use from Claude Code

With `.mcp.json` in the parent repo root, Claude Code auto-discovers the server. Tools appear as:
- `mcp__aoc__fetch_article`
- `mcp__aoc__search`
- `mcp__aoc__list_recent`
- `mcp__aoc__video_transcript`

Restart Claude Code (or `/mcp reload`) after install for first-time pickup.

## Troubleshooting

| Symptom | Fix |
|---|---|
| MCP tool returns `{code: "session_expired"}` | Run `python -m aoc_mcp.auth` to re-auth. |
| Auth CLI times out without detecting login | User didn't complete login in 5 min, or AOC changed cookie name. Inspect DevTools → Application → Cookies, add observed name(s) to `config.AUTH_COOKIE_NAMES`. |
| `playwright install chromium` fails | Check proxy/firewall. Try `PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net`. |
| Tests fail after AOC theme update | Inspect `tests/fixtures/live-article-*.html` for new selectors; update `SELECTOR_*` constants in `extract.py` / `search.py`. |
| `aoc_list_recent` returns `unknown_topic` | Update `KNOWN_TOPICS` in `config.py`. |
| Video transcript returns `null` with `captions_source: "unavailable"` | AOC's video provider doesn't expose captions for that clip. Not a bug. |

## Architecture

See `docs/superpowers/specs/2026-04-23-aoc-mcp-design.md` in the parent repo for the full design spec.
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add tools/aoc-mcp/README.md
git commit -m "docs: full README for aoc-mcp (Task 13)"
```

---

## Task 14: End-to-end proof — ingest one AOC Premium item via MCP (**INTERACTIVE**)

**Goal:** Use the MCP from Claude Code to fetch one of the originally-paywalled items flagged in Wave 1 CP2, and write the corresponding `wiki/sources/` page. This proves the full pipeline works.

**Files touched (per this task's flow):**
- Create: `raw/articles/aoc-<year>-<slug>.md`
- Create: `wiki/sources/aoc-<year>-<slug>.md`
- Modify: `raw/INDEX.md` (append entry)
- Modify: `wiki/log.md` (append ingest entry)

- [ ] **Step 1 (INTERACTIVE): User restarts Claude Code / runs `/mcp reload`**

User action: restart Claude Code or run `/mcp reload`. Verify the `aoc` MCP server shows as connected.

- [ ] **Step 2 (INTERACTIVE): User confirms MCP tools are available**

User asks Claude to `list MCP tools` or inspects via `/mcp` or similar. The four `mcp__aoc__*` tools should be visible.

- [ ] **Step 3: Agent fetches one Premium article via MCP**

In the Claude Code session (now with the MCP available), Claude runs the `mcp__aoc__fetch_article` tool on a target URL. Start with the Kiraly forearm-pass article since its fixture already exists:

```
mcp__aoc__fetch_article(url="https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/")
```

Expected return: JSON matching `ArticleResult` — `title`, `author`, `markdown`, `word_count > 100`, etc.

- [ ] **Step 4: Save the fetched content as raw + source page**

Using the returned `markdown` and metadata, write to:

`raw/articles/aoc-YYYY-kiraly-4-keys-forearm-pass.md`:
```markdown
---
source-url: https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/
fetched: 2026-04-23
raw-for: aoc-YYYY-kiraly-4-keys-forearm-pass
ingested-via: aoc-mcp
---

# <title from tool result>

<markdown body from tool result>
```

`wiki/sources/aoc-YYYY-kiraly-4-keys-forearm-pass.md`:
```yaml
---
type: source
source-type: article
title: "<title>"
author: "Karch Kiraly"
year: <year from result>
citation-key: aoc-YYYY-kiraly-4-keys-forearm-pass
raw-file: raw/articles/aoc-YYYY-kiraly-4-keys-forearm-pass.md
url: https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/
topics: [passing, forearm-pass, technique]
featured-coaches: [karch-kiraly]
schools: [art-of-coaching-volleyball, usa-volleyball-cap]
trust-tier: 2
---

# <title>

## Summary
<2-3 paragraph summary derived from the article body.>

## Key claims / ideas
<Bullets drawn from the actual article content.>

## Topics covered
<Topical breakdown.>

## Where it's cited
*(populated as wiki pages cite this source)*

## Access
- Raw file: `raw/articles/aoc-YYYY-kiraly-4-keys-forearm-pass.md`
- URL: https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/
- Trust tier: 2 — AOC Premium, named coach (Karch Kiraly)
- Ingested via: aoc-mcp at 2026-04-23
```

- [ ] **Step 5: Append entries to `raw/INDEX.md` and `wiki/log.md`**

`raw/INDEX.md` — append under `## articles/ → ### AOC (W1.5)`:
```
- aoc-YYYY-kiraly-4-keys-forearm-pass.md — Karch Kiraly's 4 Keys to the Forearm Pass (AOC Premium) — aoc-YYYY-kiraly-4-keys-forearm-pass
```

`wiki/log.md` — append:
```markdown

## [2026-04-23] aoc-mcp-e2e-proof | First MCP-driven ingest
First end-to-end use of the aoc-mcp. Ingested Kiraly's "4 Keys to the Forearm Pass"
(AOC Premium) via mcp__aoc__fetch_article. Confirms auth, fetch, extract, and wiki-write
all work over the MCP interface.
Pages touched: raw/articles/aoc-YYYY-kiraly-4-keys-forearm-pass.md,
wiki/sources/aoc-YYYY-kiraly-4-keys-forearm-pass.md, raw/INDEX.md, wiki/log.md.
```

- [ ] **Step 6: Commit the E2E proof**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
git add raw/articles/aoc-YYYY-*.md wiki/sources/aoc-YYYY-*.md raw/INDEX.md wiki/log.md
git commit -m "feat(e2e): first aoc-mcp driven wiki ingest (Task 14)"
```

- [ ] **Step 7: Final success check**

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible/tools/aoc-mcp"
source .venv/Scripts/activate
pytest -v
python -m aoc_mcp.auth --verify
```
Expected:
- All pytest tests green (~15–20 tests across extract, search, catalog, client, errors, video)
- `Session is VALID`

The MCP is live. Future ingest passes (Wave 2+) can call the `mcp__aoc__*` tools directly to pull Premium content on demand.

---

## Done criteria (from spec §10)

After Task 14, verify each bullet:

1. ✅ `python -m aoc_mcp.auth` successfully logs in → Task 5 IC1.
2. ✅ `python -m aoc_mcp.auth --verify` returns 0 for a fresh session → Task 5 IC1.
3. ✅ All 4 tools return expected-shape outputs — Task 14 validates fetch; others via pytest + manual smoke in Tasks 8–10.
4. ✅ Session-expiry path returns a structured `session_expired` error → tested in Task 4; surfaced through MCP error payload in Task 11.
5. ✅ `pytest tests/` passes ≥5 tests → by Task 10 already >15 tests.
6. ✅ `README.md` has copy-pasteable install/auth/smoke steps → Task 13.
7. ✅ `.mcp.json` in place → Task 12.
8. ✅ At least one AOC Premium item ingested via the MCP → Task 14.
