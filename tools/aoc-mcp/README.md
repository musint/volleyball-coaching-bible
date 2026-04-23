# AOC MCP

Local MCP server exposing Art of Coaching Volleyball (paid-member) content as tools for Claude Code and other MCP clients. Part of the Volleyball Coaching Bible wiki project.

## What it does

Four MCP tools:

- `aoc_fetch_article(url)` — fetch an article URL, return title/author/date/tags/markdown/word-count
- `aoc_search(query, limit=10)` — search the AOC catalog
- `aoc_list_recent(topic, limit=20)` — list recent items in a topic (`passing`, `setting`, etc.)
- `aoc_video_transcript(url)` — extract the transcript of a video page (Vimeo/Wistia captions)

## Install

Requires Python 3.11+. Disk: ~250 MB (~200 MB of that is Playwright's Chromium).

```bash
cd tools/aoc-mcp
python -m venv .venv
# Windows bash (msys / git-bash):
source .venv/Scripts/activate
# Windows cmd:
# .venv\Scripts\activate.bat
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# macOS / Linux:
# source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
playwright install chromium
```

## Auth

One-time per session lifetime (AOC cookies typically last 30–90 days). Three modes available:

### Mode 1 — Cookie-Editor extension (recommended on Windows with Chrome)

Chrome 127+ encrypts its cookie store with App-Bound Encryption (ABE), which blocks external readers even when Chrome is closed. The simplest bypass is to read cookies from within Chrome itself via a trusted extension.

1. Install the [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome extension.
2. Navigate to `theartofcoachingvolleyball.com` (logged in).
3. Click the Cookie-Editor icon → **Export** → **Export as JSON**.
4. Save the clipboard contents to a file (e.g., `cookies.json`).
5. Import:
   ```bash
   python -m aoc_mcp.auth --from-cookie-editor-json cookies.json
   ```
6. Delete the JSON file when done.

### Mode 2 — Playwright headed login

Works on systems where Cloudflare's bot challenge lets Playwright-Chromium through (varies by IP reputation, fingerprint heuristics, and whether the user has a recent session). Stealth patches are applied; real Google Chrome is preferred if installed (`channel="chrome"`), with Playwright's bundled Chromium as fallback.

```bash
python -m aoc_mcp.auth
```

Opens a visible browser. Log in manually. When Playwright detects the `wordpress_logged_in_*` cookie, it saves `.session.json` and closes the window. 5-minute timeout.

If Cloudflare blocks the Playwright browser, fall back to Mode 1 or Mode 3.

### Mode 3 — Read cookies from an installed browser

Uses `browser_cookie3` to read Chrome/Firefox/Edge/Brave's local cookie store directly. **Does not work on Chrome 127+ due to App-Bound Encryption**, but works reliably on Firefox.

```bash
# Log into AOC in Firefox, then close Firefox:
python -m aoc_mcp.auth --from-browser firefox
```

### Mode 4 — DevTools Cookie header paste

If the other paths are inconvenient, copy the `Cookie:` request header from Chrome DevTools → Network tab → (main request) → Headers → Request Headers, save to a file, and:

```bash
python -m aoc_mcp.auth --from-cookie-header cookie-header.txt
```

## Verify

```bash
python -m aoc_mcp.auth --verify
```

Prints `[auth] Session is VALID.` or `[auth] Session is EXPIRED. Run \`python -m aoc_mcp.auth\` to re-auth.`

## Refresh fixtures (dev-only)

If you need to re-capture the live AOC pages used for extractor tests:

```bash
python -m aoc_mcp.discover                                      # default seed set
python -m aoc_mcp.discover <url> <slug>                         # one-off capture
```

Saves to `tests/fixtures/<slug>.html`.

## Smoke test

```bash
pytest tests/ -v
```

Unit suite runs fully offline against fixture HTML. 38 tests covering errors, client, auth, extract, search, catalog, video.

End-to-end smoke (requires live auth):

```bash
python -c "
from aoc_mcp.client import AocClient
from aoc_mcp.extract import parse_article
url = 'https://www.theartofcoachingvolleyball.com/karch-kiralys-4-keys-to-the-forearm-pass/'
with AocClient() as c:
    r = c.get(url)
result = parse_article(r.text, url=url)
print(f'{result.title} — {result.word_count} words — author: {result.author}')
"
```

## Use from Claude Code

With `.mcp.json` at the parent repo root, Claude Code auto-discovers the server on session start. Tools appear as:

- `mcp__aoc__fetch_article`
- `mcp__aoc__search`
- `mcp__aoc__list_recent`
- `mcp__aoc__video_transcript`

Run `/mcp reload` (or restart Claude Code) to pick up the server after first install.

## Troubleshooting

| Symptom | Fix |
|---|---|
| MCP tool returns `{"code": "session_expired"}` | Re-run one of the auth modes above. |
| `[auth] Could not read chrome cookies: Unable to get key for cookie decryption` | Chrome 127+ App-Bound Encryption. Use Mode 1 (Cookie-Editor) or Mode 3 with Firefox. |
| `[auth] Auto-detect failed: This operation requires admin` | `browser_cookie3.load()` tries Volume Shadow Copy on Windows. Pass `--from-browser <name>` explicitly instead of bare `--from-browser`. |
| Cloudflare "verify you are human" page blocks Playwright login | Switch to Mode 1 (Cookie-Editor) — bypasses Cloudflare entirely since auth happens in your real, fully-trusted browser. |
| Playwright launch fails with "Executable doesn't exist" | Run `playwright install chromium` inside the venv. |
| Unit tests fail after AOC redesigns | Inspect the fresh fixture HTML (refresh via `python -m aoc_mcp.discover`), update `SELECTOR_*` constants in `aoc_mcp/extract.py` / `aoc_mcp/search.py` to match the new DOM. |
| `aoc_list_recent` returns `unknown_topic` | Update `KNOWN_TOPICS` in `aoc_mcp/config.py`. |
| Video transcript returns `{"transcript": null, "captions_source": "unavailable"}` | That video's Vimeo embed has no captions. Not a bug — graceful degradation. |
| Video transcript returns `captions_source: "unsupported_provider"` | Embed is Wistia (or another provider we don't yet handle). Wistia support is a future extension. |

## Architecture

See `docs/superpowers/specs/2026-04-23-aoc-mcp-design.md` in the parent repo for the full design spec.

Brief summary:

- **Two-phase auth.** Heavy path (Playwright / cookie import) once per session lifetime → saves `.session.json`. Every subsequent tool call uses lightweight httpx with those cookies. Session-expiry is detected on every response via a login-form sniff and surfaced as a structured MCP error.
- **Module breakdown.**
  - `client.py` — httpx fetcher with session loader + rate limit + retry + expiry sniff.
  - `auth.py` — 4 login modes (Playwright, cookie-header, cookie-editor-json, browser cookie store) + verify.
  - `discover.py` — dev tool that uses `AocClient` to save live AOC HTML as test fixtures.
  - `extract.py` — article HTML → `ArticleResult` (BeautifulSoup + markdownify).
  - `search.py` — search/archive HTML → `SearchResult`.
  - `catalog.py` — `/category/<slug>/` listing; reuses `search.py` since AOC's Genesis theme shares the archive DOM.
  - `video.py` — Playwright (headless) extracts iframe, then fetches Vimeo/Wistia captions directly.
  - `server.py` — stdio MCP bootstrap; registers 4 tools; converts `AocError` subclasses to structured MCP error payloads.
  - `errors.py` — 7-class error hierarchy with `code` field for machine-parseable MCP responses.
  - `models.py` — pydantic return types (`ArticleResult`, `SearchHit`, `SearchResult`, `VideoResult`).
  - `config.py` — constants (URLs, UA, paths, timeouts, topic map).

## Out of scope (see spec §11)

- PDF fetches (AOC hosts some printables; not handled).
- Author-based browse (use `aoc_search` with a coach name instead).
- Comment extraction.
- Video downloads (only transcripts + embed URLs are returned).
- Multi-account support — single `.session.json` per install.
- Response caching — every tool call hits AOC fresh.
- Wistia caption extraction — returns `unsupported_provider` for now.
