# AOC MCP — Design Spec

**Date:** 2026-04-23
**Owner:** Song Mu (song.mu@discordapp.com)
**Purpose:** Programmatic access to Art of Coaching Volleyball (AOC) Premium content for the Volleyball Coaching Bible wiki.
**Parent project:** `C:/Users/SongMu/documents/claudecode/vba/bible/`
**Install target:** `tools/aoc-mcp/` inside the parent project.

---

## 1. Context

### 1.1 What this is

A local Model Context Protocol (MCP) server that lets Claude Code (and any other MCP-speaking client) fetch Art of Coaching Volleyball (AOC) content on the user's behalf, using the user's own paid-member session. It is consumed by the parent project — the Volleyball Coaching Bible wiki — during source ingest and wiki research passes.

### 1.2 Why it exists

AOC's catalog includes a large body of Premium content (videos, articles, practice plans) authored by named coaches (Karch Kiraly, John Dunning, Russ Rose, etc.) that is behind a login wall. During the bootstrap sprint, ~3–5 explicitly paywalled items were flagged as content gaps. The manual alternative (Obsidian Web Clipper) works but scales poorly as the wiki grows and rewards high-volume ingest passes. The MCP automates the credentialed-fetch step.

### 1.3 Who uses it

- Primary: Claude Code sessions running inside `C:/Users/SongMu/documents/claudecode/vba/bible/` during Wave 1 backfills, Wave 2 coach/school profile writing, and any future `ingest` or `research` workflow that wants AOC Premium content.
- Secondary: any MCP-speaking client (Claude Desktop, MCP Inspector) the user points at the server.

### 1.4 Non-goals

- **Not a general web scraper.** Scope is AOC's site specifically.
- **Not a CI-tested production service.** Manual smoke tests + fixture-based extraction tests only.
- **Not distributed.** Lives in this repo's `tools/aoc-mcp/`. Not published to PyPI.
- **Not multi-user.** One session state per local install. If the user wants the MCP on another machine, they run install + auth there too.
- **No credential storage.** Password never touches disk. Session state (cookies, localStorage) is the only persistence.

### 1.5 Legal / ToS posture

AOC's Terms of Service may restrict automated access even by paying members. Before heavy use, the user is responsible for confirming compliance. The MCP is designed to minimize bot-detection surface (real-browser auth, modest request rate, single authenticated session) but it does not guarantee ToS compliance. If AOC explicitly forbids automated fetching, the user should fall back to manual Web Clipper ingest.

---

## 2. Architecture

Two-phase design: heavyweight authentication once, lightweight requests thereafter.

### 2.1 Auth phase (Playwright, headed, one-time)

`python -m aoc_mcp.auth` launches a real (headed) Chromium window via Playwright, navigates to AOC's login page, and waits for the user to complete login manually. Handles MFA, captcha, or any future auth UI change transparently because a real human drives the browser for the login step. After login, Playwright saves `storage_state.json` (cookies + localStorage) to `tools/aoc-mcp/.session.json` (gitignored). The browser closes; Playwright exits.

### 2.2 Fetch phase (httpx, headless, on-demand)

Every tool call loads `.session.json`, constructs an `httpx.Client` with the saved cookies and a realistic User-Agent, and makes an HTTP GET against AOC. No browser per request — too slow, too detectable. The client checks each response for a login-form sniff (`<form ... action="*login*">` or redirect to `/login`); if present, session is expired and the tool returns a structured `session_expired` error with a re-auth instruction.

### 2.3 Video phase (Playwright, headless, on-demand)

Video pages on AOC typically embed Vimeo or Wistia players. Extracting captions requires either the provider's oembed/captions API or, failing that, scraping the rendered page. `aoc_video_transcript()` uses Playwright in **headless** mode (no UI) to load the video page, wait for the embed iframe to load, extract the embed URL, and fetch captions via the provider's public endpoints. Playwright is loaded lazily — only when a video transcript is requested — so articles and search stay fast.

### 2.4 Runtime shape

- MCP server runs over stdio (standard for local MCPs). Claude Code launches it as a subprocess via `.mcp.json`.
- Single-process, synchronous fetch path. Concurrency at the MCP layer is provided by Claude launching multiple tool calls; each call makes its own HTTP request inside the same process. Playwright browser instance is cached between video calls to avoid repeated launches.
- No database. State is `.session.json` (auth) + in-memory caches only.

---

## 3. Components

```
tools/aoc-mcp/
  pyproject.toml                 dependencies, entry points
  README.md                      install + auth + smoke-test instructions
  .gitignore                     includes .session.json, .venv/, __pycache__
  aoc_mcp/
    __init__.py
    server.py                    MCP server bootstrap; registers 4 tools
    auth.py                      `python -m aoc_mcp.auth` CLI; Playwright headed login
    client.py                    httpx client; cookie loader; session-expiry sniff
    extract.py                   AOC article HTML → markdown
    search.py                    aoc_search() impl
    catalog.py                   aoc_list_recent() impl
    video.py                     aoc_video_transcript() impl (lazy Playwright)
    errors.py                    structured error types (SessionExpired, NotFound, RateLimited, ParserFailed)
    config.py                    paths, constants, AOC base URL, UA string
  tests/
    __init__.py
    fixtures/                    saved AOC HTML snapshots for extract tests
      sample-article.html
      sample-search-results.html
      sample-topic-page.html
    test_extract.py              pytest: HTML → markdown correctness
    test_client.py               pytest: session-expiry sniff, cookie loader
  .session.json                  Playwright state (gitignored)
```

### 3.1 `config.py`

Constants only, no logic.
- `AOC_BASE_URL = "https://www.theartofcoachingvolleyball.com"`
- `AOC_LOGIN_URL = f"{AOC_BASE_URL}/login"`
- `SESSION_FILE = Path(__file__).parent.parent / ".session.json"`
- `USER_AGENT = <a Chrome 120+ UA string, updated manually when it ages>`
- `DEFAULT_TIMEOUT_S = 30`
- `REQUEST_MIN_INTERVAL_S = 1.0` (rate limit: 1 req/sec min)

### 3.2 `auth.py` — CLI

Entry point: `python -m aoc_mcp.auth [--verify]`.

Two modes:
- **Default (login mode):** launches headed Chromium, navigates to AOC login URL. Waits for user to log in. Detects login completion by polling for a cookie name (e.g., `wordpress_logged_in_*` or AOC's session cookie — determined during implementation by inspecting the real site). On detection, calls `context.storage_state(path=SESSION_FILE)`, prints confirmation, exits 0.
- **`--verify` mode:** loads `.session.json` (if present), makes one authenticated HEAD request against a known-authenticated AOC page. Exits 0 if session is valid, nonzero if expired or missing.

Login-completion detection has a 5-minute timeout. If the user walks away without logging in, the CLI exits with an error.

### 3.3 `client.py` — HTTP fetcher

Single class `AocClient`:

```python
class AocClient:
    def __init__(self):                     # loads session.json into httpx cookies
    def get(self, url: str) -> httpx.Response:  # with session-expiry sniff
    def _check_not_logged_out(self, r) -> None: # raises SessionExpired if login form detected
```

Session-expiry sniff:
1. Response URL redirected to `/login` or `/wp-login.php` → expired.
2. Response body contains `<form ... id="loginform"` or AOC's login form signature → expired.
3. Response is 200 with expected article wrapper → OK.

The client throttles: minimum 1.0 seconds between requests (`REQUEST_MIN_INTERVAL_S`). Retries 429/503 once with exponential backoff (1s, then 4s).

### 3.4 `extract.py` — article HTML → markdown

Input: raw HTML string. Output: `ArticleResult` pydantic model.

```python
class ArticleResult(BaseModel):
    title: str
    author: str | None
    date: str | None         # ISO-8601 or ""
    tags: list[str]
    markdown: str            # article body only, no site chrome
    word_count: int
    url: str
```

Strategy:
1. Parse with BeautifulSoup.
2. Extract title from `<h1>` inside the main article container.
3. Extract author from a byline element (AOC's typical pattern — selector determined from fixtures).
4. Extract date from `<time>` or meta tag.
5. Extract tags from tag-list element.
6. Isolate the article body container, strip known chrome classes (ad boxes, social buttons, related-posts blocks, author bios, paywall-prompts-stripped-for-paid-users but defensively re-stripped).
7. Convert body to markdown via `markdownify` with `heading_style="ATX"`, stripping `<script>`, `<style>`, `<iframe>` (except video embeds we want to preserve as links), `<noscript>`.
8. Count words in the resulting markdown.

If the container structure isn't found (AOC changed DOM), raise `ParserFailed` with a snippet of the raw HTML so the user/agent can adapt.

### 3.5 `search.py` — catalog search

AOC exposes a search endpoint (confirmed during implementation via site inspection). Most likely pattern: `GET /?s=<query>` or `/search?q=<query>` returning a results page.

`aoc_search(query, limit=10)` flow:
1. Build search URL, GET via `AocClient`.
2. Parse results page, extract result cards (title, url, author, snippet, date).
3. Return first `limit` results.
4. If no results, return empty list (not error).

Output shape:

```python
class SearchHit(BaseModel):
    title: str
    url: str
    author: str | None
    snippet: str
    date: str | None
```

### 3.6 `catalog.py` — topic/category listing

AOC organizes content under topic URLs like `/category/passing/` or `/topic/setting/` (exact path-structure determined during implementation).

`aoc_list_recent(topic, limit=20)` flow:
1. Map topic slug to AOC category URL. Known topic slugs: `passing`, `setting`, `hitting`, `blocking`, `serving`, `defense`, `transition`, `practice-planning`, `season-planning`, `mental`, `physical`, `match-prep`, `recruiting`. List is extended as AOC's taxonomy is explored during implementation.
2. GET the topic URL via `AocClient`.
3. Parse result cards. Paginate if needed to reach `limit`.
4. Return items in reverse-chronological order.

Output uses the same `SearchHit` shape as search.

### 3.7 `video.py` — video transcript

`aoc_video_transcript(url)` flow:
1. Load `.session.json` into a Playwright BrowserContext (headless).
2. Navigate to the AOC video page URL.
3. Wait for embedded video iframe to render.
4. Extract the embed URL from the `<iframe src="...">` attribute.
5. Detect provider: Vimeo (`player.vimeo.com`) or Wistia (`fast.wistia.net`). Other providers → return `{transcript: null, captions_source: "unsupported_provider"}`.
6. For Vimeo: call `https://vimeo.com/<video_id>/texttrack/<lang>.vtt` (requires the user's session being auth'd on Vimeo, OR the video being embed-accessible). Parse VTT, concatenate into transcript string.
7. For Wistia: hit the Wistia captions endpoint discovered during implementation.
8. Also extract title/author/duration from the AOC page metadata.

Output:

```python
class VideoResult(BaseModel):
    title: str
    author: str | None
    duration_sec: int | None
    transcript: str | None   # None if unavailable
    captions_source: str     # "vimeo" | "wistia" | "unavailable" | "unsupported_provider"
    embed_url: str | None
    url: str
```

Playwright browser context is lazily created on first video call and cached in a module-level variable for the lifetime of the MCP server process. On process exit, cleanup runs. If an open context errors out, next call recreates it.

### 3.8 `errors.py`

Structured error types that serialize cleanly through MCP's error channel.

```python
class AocError(Exception): ...
class SessionExpired(AocError): ...
class NotFound(AocError): ...
class RateLimited(AocError): ...
class ParserFailed(AocError):
    def __init__(self, url, snippet): ...
class UnsupportedProvider(AocError): ...
```

`server.py` catches `AocError` subclasses and converts to MCP error responses with clear `code` and `message` fields. Unknown exceptions propagate as generic errors (with traceback in debug mode).

### 3.9 `server.py` — MCP bootstrap

Uses the official `mcp` Python package (`pip install mcp`). Registers exactly 4 tools with the names Claude will call:

| Tool name (as seen by Claude) | Internal function |
|---|---|
| `mcp__aoc__fetch_article` | `extract.fetch_article(url)` |
| `mcp__aoc__search` | `search.run(query, limit)` |
| `mcp__aoc__list_recent` | `catalog.list_recent(topic, limit)` |
| `mcp__aoc__video_transcript` | `video.get_transcript(url)` |

Server uses stdio transport (`mcp.server.stdio.stdio_server`). On startup, verifies `.session.json` exists; if not, all tool calls return `SessionExpired` error with an actionable message.

---

## 4. Tool contracts

### 4.1 `aoc_fetch_article(url: str)`

**Input:**
```json
{ "url": "https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/" }
```

**Success output:**
```json
{
  "title": "Karch Kiraly's 4 Keys to the Forearm Pass",
  "author": "Karch Kiraly",
  "date": "2019-03-12",
  "tags": ["passing", "technique"],
  "markdown": "# Karch Kiraly's 4 Keys to the Forearm Pass\n\n...",
  "word_count": 1842,
  "url": "https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/"
}
```

**Error outputs** (structured MCP error):
- `{code: "session_expired", message: "Re-authenticate: run `python -m aoc_mcp.auth` from tools/aoc-mcp/"}`
- `{code: "not_found", message: "<url> returned 404"}`
- `{code: "parser_failed", message: "<url>", snippet: "<first 500 chars of HTML>"}`

### 4.2 `aoc_search(query: str, limit: int = 10)`

**Input:**
```json
{ "query": "karch passing", "limit": 10 }
```

**Success output:**
```json
{
  "hits": [
    {
      "title": "Karch Kiraly's 4 Keys to the Forearm Pass",
      "url": "https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/",
      "author": "Karch Kiraly",
      "snippet": "Karch walks through his four keys for training and teaching...",
      "date": "2019-03-12"
    }
  ],
  "total_returned": 1
}
```

### 4.3 `aoc_list_recent(topic: str, limit: int = 20)`

**Input:**
```json
{ "topic": "passing", "limit": 20 }
```

**Success output:** Same shape as `aoc_search`.

**Error:** `{code: "unknown_topic", message: "<topic> not in known-topic list", known_topics: [...]}`

### 4.4 `aoc_video_transcript(url: str)`

**Input:**
```json
{ "url": "https://www.theartofcoachingvolleyball.com/video/karch-kiraly-passing-masterclass-ep1/" }
```

**Success output:**
```json
{
  "title": "Karch Kiraly Passing Masterclass — Episode 1",
  "author": "Karch Kiraly",
  "duration_sec": 1423,
  "transcript": "WEBVTT header stripped...\n\nKarch: One of the things I want to talk about today...",
  "captions_source": "vimeo",
  "embed_url": "https://player.vimeo.com/video/123456789",
  "url": "https://www.theartofcoachingvolleyball.com/video/karch-kiraly-passing-masterclass-ep1/"
}
```

When transcript is unavailable (e.g., Vimeo has no captions), the shape is the same but `transcript` is `null` and `captions_source` reflects the reason (`"unavailable"`, `"unsupported_provider"`). This is not an error — the caller gets metadata and decides what to do.

---

## 5. Data flow — end-to-end examples

### 5.1 First-time user setup

```
user: cd tools/aoc-mcp
user: python -m venv .venv
user: source .venv/Scripts/activate          # Windows bash; use .venv\Scripts\activate on Windows cmd
user: pip install -e .
user: playwright install chromium             # ~200MB, one-time
user: python -m aoc_mcp.auth
     → Chromium window opens at AOC login
     → user logs in (email + password, MFA if any)
     → Playwright detects auth cookie, saves .session.json
     → window closes, CLI prints "Authenticated. Session saved to .session.json"
user: exit venv (MCP runs under Claude Code, which spawns its own venv-less python)
user: verify .mcp.json is in repo root pointing at tools/aoc-mcp
user: restart Claude Code (or run /mcp reload)
```

### 5.2 Claude Code using the MCP during ingest

```
assistant: (calls mcp__aoc__fetch_article(url="https://theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/"))
mcp server: loads .session.json → httpx GET with cookies → receives 200 + article HTML
             → checks for login form (not present) → passes HTML to extract.py
             → returns ArticleResult JSON
assistant: writes raw/articles/aoc-2019-kiraly-forearm-pass-4-keys.md with fetched markdown
           writes wiki/sources/aoc-2019-kiraly-forearm-pass-4-keys.md with source page template
           updates wiki/log.md with ingest entry
```

### 5.3 Session expired mid-session

```
assistant: (calls mcp__aoc__fetch_article(url="..."))
mcp server: loads .session.json → httpx GET → response redirects to /login
             → raises SessionExpired
             → MCP returns error: { code: "session_expired", message: "Re-authenticate: run `python -m aoc_mcp.auth` from tools/aoc-mcp/" }
assistant: reports error to user: "AOC session expired — please run `python -m aoc_mcp.auth` from tools/aoc-mcp/, then I'll retry."
user: runs auth, confirms re-login
assistant: retries the call successfully
```

---

## 6. Error handling

All errors route through `errors.py` and become structured MCP errors. The contract is: Claude always sees a clean `{code, message, ...}` payload, never a raw Python traceback.

| Situation | Error code | User action |
|---|---|---|
| `.session.json` missing or empty | `session_expired` | Run `python -m aoc_mcp.auth` |
| Response redirects to login | `session_expired` | Re-auth |
| HTTP 404 | `not_found` | Verify URL; may be dead link |
| HTTP 429 after one retry | `rate_limited` | Wait, or investigate if Claude is hammering |
| HTTP 5xx after one retry | `upstream_error` | AOC is down; retry later |
| Parser can't find article body | `parser_failed` | Investigate — AOC may have changed DOM |
| Video page has no supported embed | `unsupported_provider` | Fallback to manual clip |
| Playwright launch fails | `runtime_error` | Check `playwright install chromium` ran |
| Unknown topic slug | `unknown_topic` (with `known_topics` list) | Pick from list |

Rate-limit strategy: minimum 1.0 second between any two requests. Retry once on 429/503 with backoff (1s then 4s). If still failing, return error rather than hammer. This keeps the MCP a good citizen even if Claude spams calls.

---

## 7. Testing

Two test categories:

### 7.1 Fixture-based extraction tests (CI-friendly, no live network)

`tests/test_extract.py` loads HTML from `tests/fixtures/` (hand-saved AOC pages, scrubbed of PII) and asserts:
- `fetch_article` on `sample-article.html` returns expected title, author, date, tags
- Markdown output contains expected headings + paragraphs
- Word count is within ±10% of expected
- `search.parse` on `sample-search-results.html` extracts expected hit count + first hit
- `catalog.parse` on `sample-topic-page.html` extracts expected items

Run: `pytest tools/aoc-mcp/tests/` — no network, no auth required.

### 7.2 Manual smoke tests (live, doc'd in README)

Documented step-by-step in `tools/aoc-mcp/README.md`:
1. `python -m aoc_mcp.auth --verify` → prints "session valid" or "session expired"
2. Use MCP Inspector or a tiny test script to call each of the 4 tools against a known URL. Verify output shape + non-empty content.
3. Test session-expiry path: delete `.session.json`, call a tool, verify structured `session_expired` error.

No live-AOC tests in CI (would require live creds + risk ToS).

---

## 8. Install, config, and operational detail

### 8.1 `.mcp.json` (repo root)

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

Windows path shown above (project is developed on Windows). If the user develops on macOS/Linux, substitute `tools/aoc-mcp/.venv/bin/python`. Using the venv's Python directly (rather than `"command": "python"`) avoids ambiguity about which Python Claude Code's subprocess inherits and guarantees `aoc_mcp` (installed via `pip install -e .`) resolves. Claude Code discovers this file automatically on session start; `/mcp reload` picks up changes without restart.

### 8.2 `tools/aoc-mcp/pyproject.toml`

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

[project.scripts]
aoc-auth = "aoc_mcp.auth:main"

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23"]
```

### 8.3 `.gitignore` (inside `tools/aoc-mcp/`)

```
.venv/
__pycache__/
*.pyc
.session.json
.pytest_cache/
```

The root `.gitignore` does NOT need to change — the nested gitignore covers `.session.json`.

### 8.4 User-visible footprint

- New directory: `tools/aoc-mcp/` (committed)
- New file: `.mcp.json` at repo root (committed)
- Playwright Chromium install: `~/.cache/ms-playwright/chromium-*` (not in repo, ~200MB)
- User's Python virtualenv: `tools/aoc-mcp/.venv/` (gitignored)
- User's auth state: `tools/aoc-mcp/.session.json` (gitignored)

---

## 9. Open questions (resolve during implementation)

These require live site inspection and are not decidable from spec alone:

1. **AOC's actual session-cookie name(s).** Needed for login-completion detection in `auth.py`.
2. **AOC's article DOM selectors** (title, author, date, tags, body container). Needed for `extract.py`. Fixtures will be captured from the live site during implementation and committed to `tests/fixtures/`.
3. **AOC's search URL format.** Likely WordPress-standard `/?s=` but requires confirmation.
4. **AOC's category URL format.** Likely `/category/<slug>/` but requires confirmation.
5. **Video hosting provider(s) AOC uses.** Likely Vimeo; Wistia is a secondary possibility. Other providers (JW Player, native HTML5) would need added support.
6. **Whether AOC uses any anti-bot protection** (Cloudflare Under Attack, PerimeterX, etc.) that would break httpx-level fetches and force full-Playwright mode for articles too.

Each open question becomes a discovery task in the implementation plan; the plan may adjust extraction selectors and endpoint paths based on what's found.

---

## 10. Success criteria

The MCP ships when all of the following hold:

1. `python -m aoc_mcp.auth` successfully logs in and saves `.session.json` on the user's machine.
2. `python -m aoc_mcp.auth --verify` returns 0 for a fresh session.
3. All 4 tools return expected-shape outputs against at least one known-good URL each (the 3 flagged AOC Premium items from Wave 1 CP2 plus one video).
4. Session-expiry path returns a structured `session_expired` error with the re-auth instruction visible to Claude.
5. `pytest tools/aoc-mcp/tests/` passes with at least 5 tests green.
6. `tools/aoc-mcp/README.md` contains copy-pasteable install + auth + smoke-test steps that work on a clean machine.
7. `.mcp.json` is in place and Claude Code discovers the server on restart.
8. The MCP is used to ingest at least one AOC Premium item into `wiki/sources/` as a live end-to-end proof.

---

## 11. Out of scope

Explicitly deferred:
- **PDF fetches.** If AOC hosts PDFs (practice plans, printables), a `aoc_fetch_pdf(url)` tool would need binary handling. Not included.
- **Author-based browse** (`aoc_list_by_author`). Covered indirectly by `aoc_search(query="<coach name>")`.
- **Comment extraction.** Premium-article comment threads may contain useful coach-to-coach dialogue; ignore for now.
- **Video-download.** The MCP returns transcripts and embed URLs but does NOT download video files.
- **Multi-account support.** Single `.session.json` per install.
- **Caching / memoization.** No response cache in this version. If the same URL is fetched twice, two network requests happen. Future optimization.
- **Observability.** No structured logging, no metrics. Errors print to stderr; happy path is silent.
