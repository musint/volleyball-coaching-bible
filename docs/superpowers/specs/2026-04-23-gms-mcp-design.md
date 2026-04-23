# gms-mcp — Design Spec

**Date:** 2026-04-23
**Status:** Draft for implementation
**Sibling project:** `tools/aoc-mcp/` (The Art of Coaching Volleyball MCP)

## Purpose

Build a second MCP server, `gms-mcp`, that ingests content from the Gold Medal Squared
community site (`community.goldmedalsquared.com`) into this wiki's `raw/` tree. GMS
runs on Circle.so; the user is a paying member with access to premium spaces including
`articles-premium`. The MCP surfaces member-gated content — articles, drill/practice
posts, video posts, webinars, forum threads, and PDF attachments — as ingest-ready
markdown files that slot into the existing wiki source-prefixed layout alongside
`aoc-*` content.

This MCP is sibling to `aoc-mcp` and deliberately mirrors its patterns (Cookie-Editor
JSON auth, fixture-replay tests, stdio server, source-prefixed filenames) where the
Circle platform does not force a different approach.

## Platform

Confirmed via fingerprinting (Rails + Turbo + Stimulus headers, `circle.so` references
in markup, `og:site_name=GMS`, Cloudflare in front). The site has an internal JSON API
(`/api/v1/*`) that accepts session-cookie auth and returns clean post/space/comment
JSON. This API is not a documented public contract, so the design treats it as a
private surface guarded by fixture-replay tests.

## Non-goals

- **No Playwright fallback.** The JSON API is the only path. If it breaks, adding a
  Playwright scraping path is a day of work; there is no value in building it up-front.
- **No incremental/delta sync.** Fetch-by-URL is sufficient; higher-level batch scripts
  can loop over `gms_list_recent`.
- **No engagement metrics** (reactions, views, bookmarks). Low-signal for wiki use.
- **No auto re-auth.** When cookies expire, the MCP returns an actionable error telling
  the user to re-export cookies from the Cookie-Editor extension. Matches aoc-mcp.
- **No Circle Admin API / Headless API token support.** Session-cookie path only, to
  match what a regular member has access to.
- **No comment threading deeper than 3 levels.** Circle allows arbitrary depth; we
  flatten at depth 3. Rare in practice, and ugly in markdown.

## User-facing decisions (locked during brainstorming)

| Decision | Value |
|---|---|
| Purpose | Wiki ingestion + GMS-specific content types |
| Auth | Cookie-Editor JSON import only (same as aoc-mcp) |
| Scope | All spaces the signed-in user can read (enumerated via API) |
| Output layout | Source-prefixed filenames in shared `raw/` dirs |
| Approach | Circle internal JSON API (no HTML scraping, no fallback) |

## Architecture

### Package layout

```
tools/gms-mcp/
  gms_mcp/
    __init__.py
    auth.py          # Cookie-Editor JSON → requests.Session; detect expiry
    client.py        # Circle API client: authenticated GET/paginate
    spaces.py        # list + resolve spaces (id ↔ slug ↔ name)
    search.py        # /api/v1/search across accessible spaces
    extract.py       # post JSON → markdown + front matter; content-type detection
    comments.py      # flatten nested comment trees → threaded markdown
    attachments.py   # download PDFs/files to raw/pdfs/
    video.py         # Mux transcripts + reuse of aoc-mcp Vimeo/Wistia logic
    models.py        # Space, Post, Comment, Attachment, VideoEmbed dataclasses
    server.py        # MCP stdio server exposing the 5 tools
    config.py        # env resolution (GMS_COOKIES_PATH, etc.)
    errors.py        # actionable errors (expired auth, missing cookie, API drift)
    discover.py      # capture live fixtures for tests (mirrors aoc-mcp pattern)
  tests/
    fixtures/        # small committed JSON; larger bodies gitignored
    test_extract.py
    test_comments.py
    test_attachments.py
    test_video.py
    test_e2e.py      # --live flag
  pyproject.toml
  README.md
```

### Reuse from aoc-mcp

- **Cookie-Editor JSON import pattern** — same code shape in `auth.py`, different
  cookie-domain filter (`community.goldmedalsquared.com`).
- **Fixture-replay test approach** — `discover.py` captures live responses once; unit
  tests replay fixtures, never hit the network.
- **MCP stdio server shape** — `server.py` registers tools and delegates to pure
  functions in the other modules.
- **Vimeo/Wistia transcript extraction** — `video.py` imports the existing
  `aoc_mcp.video` logic where video providers overlap.

### Circle API endpoints used

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/community_members/me.json` | Auth check; detect expired session |
| `GET /api/v1/spaces.json` | Enumerate all spaces the user can read |
| `GET /api/v1/posts.json?space_id=N&page=P` | List posts in a space, paginated |
| `GET /api/v1/posts/<id>.json` | Full post JSON (body as Tiptap/ProseMirror HTML) |
| `GET /api/v1/posts/<id>/comments.json` | Nested comments tree |
| `GET /api/v1/search?q=<query>` | Full-text search |

All calls carry the session cookies loaded from the Cookie-Editor export.

## MCP tool surface

Five tools registered over stdio:

### 1. `gms_list_spaces`
**Args:** none
**Returns:** list of `{id, slug, name, post_count, space_group}`
**Purpose:** discoverability — tells callers what spaces exist without forcing them to
know Circle slugs up-front.

### 2. `gms_list_recent`
**Args:** `space` (slug, optional), `limit` (default 20, max 100), `since` (ISO date, optional)
**Returns:** list of `{id, slug, title, author, published_at, space, url, comment_count}`
**Purpose:** incremental discovery of new content. With no `space`, returns recent
posts across all accessible spaces.

### 3. `gms_search`
**Args:** `query` (required), `space` (slug, optional), `limit` (default 20, max 50)
**Returns:** same shape as `gms_list_recent`
**Purpose:** targeted retrieval by keyword (e.g., "passing platform", "4-2 offense").

### 4. `gms_fetch_post`
**Args:** `url_or_slug` (required; accepts full Circle URL or `<space-slug>/<post-slug>`)
**Returns:** `{post_id, raw_paths: [...], content_type, attachments, video}`
**Side effects:** writes one markdown file to `raw/articles/gms-*.md`, downloads any
PDFs to `raw/pdfs/gms-*.pdf`, and if a video embed is present, triggers
`gms_video_transcript` and writes to `raw/transcripts/gms-*.md`.
**Purpose:** one call = one ingest-ready package for a single post.

### 5. `gms_video_transcript`
**Args:** `url` (required; Circle post URL or bare video URL)
**Returns:** `{provider, id, transcript_path}` or `{provider, id, transcript_unavailable: true}`
**Side effects:** writes `raw/transcripts/gms-*.md` if a transcript is available.
**Purpose:** standalone transcript pull. Mirrors aoc-mcp's `aoc_video_transcript`.

## Content-type detection

Applied once per post during `extract.py`. Lightweight heuristics over the post JSON —
the goal is useful labels, not a taxonomy.

| Signal | Classification |
|---|---|
| Plain-text body under 200 characters AND exactly one video embed | `video` |
| Any attachment with extension `.pdf`/`.docx`/`.xlsx`/`.pptx` | adds `document` marker (non-exclusive) |
| Comment count > 0 AND body is short or question-shaped (`?` in first sentence, <400 chars) | `forum_thread` |
| Space slug contains `drill` or `practice` OR body has a heading matching `Setup`/`Reps`/`Progression` | `drill` |
| Space slug contains `webinar`/`live`/`clinic` OR body has a long video + explicit timestamps | `webinar` |
| None of the above | `article` |

`content_type` is the primary label; `has_document: true` rides alongside in
front-matter. A drill with a video and a PDF gets `content_type: drill`, plus a video
transcript file, plus a PDF in `raw/pdfs/`.

## Output files

### Primary markdown

Path: `raw/articles/gms-<slug>.md`. On slug collision across spaces, the writer
checks for an existing file before writing. If the existing file's front-matter has a
different `post_id`, both files are renamed to the disambiguated form
`raw/articles/gms-<space-slug>-<post-slug>.md`. If the `post_id` matches, the existing
file is overwritten (re-ingest).

Front-matter (YAML):

```yaml
---
source: gms
space: articles-premium
space_id: 12345
post_id: 67890
slug: 4-2-plan-for-first-11s-tournament
url: https://community.goldmedalsquared.com/c/articles-premium/4-2-plan-for-first-11s-tournament
author: Full Name
published_at: 2024-09-15T12:34:56Z
content_type: article   # article | forum_thread | drill | video | webinar
has_document: false
tags: [offense, 4-2]
attachments:
  - filename: gms-<slug>-playbook.pdf
    raw_path: raw/pdfs/gms-<slug>-playbook.pdf
video:
  provider: mux
  id: abc123
  transcript_path: raw/transcripts/gms-<slug>.md
comments_included: true
ingested_at: 2026-04-23
---
```

Body follows: markdown converted from Circle's Tiptap/ProseMirror HTML, then optional
`## Comments` section with comments threaded by depth via blockquote nesting
(`>` at depth 1, `>>` at depth 2, `>>>` at depth 3; anything deeper is flattened to
depth 3).

### Attachments

Downloaded to `raw/pdfs/` (new directory). A `.gitkeep` and a one-line description in
`raw/INDEX.md` explain what the directory is for. Signed S3 URLs from Circle expire,
so we download eagerly during `gms_fetch_post`.

Size guard: attachments >25MB are skipped with a logged error and the signed URL
recorded in front-matter for manual retrieval.

### Video transcripts

`raw/transcripts/gms-<slug>.md`. Same front-matter shape as aoc-mcp transcripts so
downstream wiki pipelines don't have to distinguish.

## Auth

`GMS_COOKIES_PATH` env var points to a Cookie-Editor JSON export for
`community.goldmedalsquared.com`. `auth.py` loads the JSON, filters cookies by domain,
and builds a reusable `requests.Session`. First API call after session construction
hits `/api/v1/community_members/me.json` to verify; any 401/403 raises
`AuthExpiredError` with instructions to re-export cookies.

Cookie JSON path is configured per MCP installation; users on different machines point
the env var at their own local export. Cookies are never committed.

## Testing

### Fixture-replay unit tests (no network)

`discover.py` captures live responses into `tests/fixtures/` for one example of each
content type:

- plain article
- drill with structured sections
- video post (Mux embed)
- forum thread with nested comments
- webinar (long video + timestamps)
- post with PDF attachment

Committed fixtures are small (post JSON, spaces JSON, search JSON). Larger bodies
(full HTML, PDFs) are gitignored. Tests assert on markdown output, front-matter keys,
content-type detection, and comment flattening.

### E2E smoke test

One `test_e2e.py` hits the live site and runs `gms_fetch_post` on one known-stable
post. Skipped by default; runs with `pytest --live`. Mirrors aoc-mcp Task 14.

## Project integration

### `.mcp.json`

Add a second entry alongside `aoc`:

```json
{
  "mcpServers": {
    "aoc": {
      "command": "tools/aoc-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "aoc_mcp.server"]
    },
    "gms": {
      "command": "tools/gms-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "gms_mcp.server"],
      "env": {"GMS_COOKIES_PATH": "<user-provided path>"}
    }
  }
}
```

Tools surface as `mcp__gms__gms_*` after Claude Code restart.

### `raw/INDEX.md`

Add a GMS section listing ingested content (parallel to any existing AOC section).
Add a one-line description of the new `raw/pdfs/` directory.

### `wiki/log.md`

Log each ingest batch (date, counts, source) — existing pattern for aoc-mcp.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Circle internal API endpoints change | Fixture-replay tests fail fast; swap path if needed |
| Mux transcripts not always available | Fall back to placeholder; record provider/id for retry |
| Large PDFs (>25MB) | Size guard skips download, logs signed URL for manual grab |
| Session cookies expire mid-batch | `AuthExpiredError` with re-export instructions; resumable by URL |
| Slug collision across spaces | Collision detector falls back to `gms-<space>-<slug>.md` |
| Body HTML uses Circle-specific widgets we don't render | Unknown widgets serialize as a markdown link + comment; never silently dropped |

## Open items for plan phase

- Exact Tiptap/ProseMirror → markdown conversion library choice
  (`html2text` vs `markdownify` vs custom) — decide after fixture capture
- Whether to paginate `gms_search` results or cap at 50 — confirm Circle's response shape
- Mux transcript API auth — verify whether a Mux playback ID plus community session is
  sufficient, or if we need a separate Mux env var
