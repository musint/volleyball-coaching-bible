"""Extract video transcripts from AOC video pages.

Flow:
  1. Load the AOC page in headless Playwright (JS renders the iframe) using the
     saved AOC session so Premium videos render.
  2. Extract the embedded Vimeo/Wistia URL from the <iframe src="...">.
  3. For Vimeo: call the player config to get caption URLs, fetch VTT, strip to plain text.
  4. For Wistia: returns unsupported for now (follow-up task).
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


async def _extract_embed_from_page(page_url: str) -> tuple[Optional[str], str, Optional[str]]:
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

        # Title — strip AOC suffix
        title = await page.title()
        title = re.sub(r"\s*[-|]\s*Art of Coaching Volleyball\s*$", "", title)

        # Author — try a few selectors
        author: Optional[str] = None
        for sel in [".entry-authorname a", ".author.vcard a", ".byline .author", ".entry-meta .author"]:
            el = await page.query_selector(sel)
            if el:
                txt = (await el.text_content() or "").strip()
                if txt:
                    author = txt
                    break

        # Embed URL from iframe src
        iframes = await page.query_selector_all("iframe")
        embed_url: Optional[str] = None
        for ifr in iframes:
            src = await ifr.get_attribute("src") or ""
            if "vimeo.com" in src or "wistia" in src:
                embed_url = src
                break

        await browser.close()
        return embed_url, title, author


def _detect_provider(embed_url: str) -> Optional[tuple[str, str]]:
    """Return (provider_name, provider_id) or None."""
    if m := VIMEO_RE.search(embed_url):
        return "vimeo", m.group(1)
    if m := WISTIA_RE.search(embed_url):
        return "wistia", m.group(1)
    return None


async def _fetch_vimeo_captions(video_id: str) -> Optional[str]:
    """Try to fetch Vimeo captions via the public config API.

    Vimeo exposes video configs at https://player.vimeo.com/video/<id>/config.
    The config JSON may include `request.text_tracks` with caption URLs. The
    endpoint may require a Referer header matching the embedding site.
    Returns plain-text transcript, or None if captions unavailable.
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
