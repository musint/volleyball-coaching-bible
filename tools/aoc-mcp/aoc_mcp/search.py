"""Parse AOC search-results HTML into SearchResult.

AOC uses a Genesis child theme on WordPress. Both search-results pages and
category archive pages render each post as an `<article class="post-* ... entry">`
inside `div.archive-inner`. Captured from the live `live-search-karch.html`
fixture (2026-04, ~430 KB).

Observed DOM per result item:

    <article class="post-<ID> ... entry" aria-label="...">
      <div class="entry-feature">
        <span class="entry-date">October 20, 2024</span>
        <a href="<permalink>" class="image-link">
          <img class="alignnone post-image" alt="..." />
        </a>
      </div>
      <header class="entry-header">
        <h2 class="entry-title" itemprop="headline">
          <a class="entry-title-link" rel="bookmark" href="<permalink>">
            <title text>
          </a>
        </h2>
      </header>
      <div class="entry-content" itemprop="text">
        <div class="entry-meta">
          <span class="entry-views">1922 views</span>
        </div>
      </div>
      <footer class="entry-footer"></footer>
    </article>

Notes:
- There is NO author byline on search/archive pages. `hit.author` stays None.
- There is NO excerpt — AOC's archive renders the thumbnail + title + views
  only. We leave `hit.snippet` empty; the `karch` substring match still hits
  via titles.
- The date is human-readable ("October 20, 2024") without a `datetime`
  attribute; we pass it through verbatim as the test suite only asserts its
  presence is acceptable (it may be non-ISO).

This parser is reused by `catalog.py` (Task 9) because WordPress renders the
same DOM for search and category archives.
"""
from __future__ import annotations

from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup

from aoc_mcp import config
from aoc_mcp.client import AocClient
from aoc_mcp.models import SearchHit, SearchResult

# Repeating-result wrapper. AOC's Genesis child theme (`coaching_vb`) wraps
# each archive/search hit in `<article class="post-<ID> ... entry">`. Keep
# fallbacks for other Genesis/WP skins in case a theme update shifts classes.
SELECTOR_RESULT_ITEM = (
    "div.archive-inner article.post, "
    "article.post.entry, "
    "article.hentry, "
    "div.single-loop, "
    ".search-result"
)

# Title link lives inside `<h2 class="entry-title"> > <a class="entry-title-link">`
# on AOC archives. Keep Genesis-generic fallbacks after that.
SELECTOR_ITEM_TITLE = (
    "h2.entry-title a.entry-title-link, "
    "h2.entry-title a, "
    "h3.entry-title a, "
    ".entry-title a, "
    "a.entry-title-link"
)

# No snippet/excerpt on AOC search pages — selectors kept as fallbacks in
# case a future theme variant renders excerpts on archives.
SELECTOR_ITEM_SNIPPET = ".entry-summary, .entry-content p, .post-excerpt"

# Author byline. Absent on AOC search results, kept for forward-compat.
SELECTOR_ITEM_AUTHOR = (
    ".entry-authorname a, .author.vcard a, .byline .author"
)

# Date: AOC uses `<span class="entry-date">Month D, YYYY</span>` on archives
# (no `datetime` attribute). Include <time> selectors for other themes.
SELECTOR_ITEM_DATE = "span.entry-date, .entry-date, time.published, time.entry-time"


def _snippet_squeeze(text: str, *, max_len: int = 300) -> str:
    """Trim whitespace-collapsed snippet to `max_len` on a word boundary."""
    collapsed = " ".join(text.split())
    if len(collapsed) <= max_len:
        return collapsed
    return collapsed[:max_len].rsplit(" ", 1)[0] + "…"


def parse_search_results(html: str, *, limit: int = 10) -> SearchResult:
    """Parse AOC search/archive HTML into a SearchResult.

    Returns an empty SearchResult when no items match — search pages may
    legitimately have 0 hits, so we don't raise.
    """
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(SELECTOR_RESULT_ITEM)

    hits: list[SearchHit] = []
    for item in items:
        if len(hits) >= limit:
            break

        title_el = item.select_one(SELECTOR_ITEM_TITLE)
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        if not title or not href:
            continue
        url = urljoin(config.AOC_BASE_URL, href)

        snippet_el = item.select_one(SELECTOR_ITEM_SNIPPET)
        snippet = _snippet_squeeze(snippet_el.get_text(" ", strip=True)) if snippet_el else ""

        author_el = item.select_one(SELECTOR_ITEM_AUTHOR)
        author = author_el.get_text(strip=True) if author_el else None

        date_el = item.select_one(SELECTOR_ITEM_DATE)
        date: str | None = None
        if date_el:
            iso = date_el.get("datetime")
            if iso:
                # Keep YYYY-MM-DD prefix when an ISO timestamp is present.
                date = iso[:10]
            else:
                text = date_el.get_text(strip=True)
                date = text or None

        hits.append(
            SearchHit(
                title=title,
                url=url,
                author=author,
                snippet=snippet,
                date=date,
            )
        )

    return SearchResult(hits=hits, total_returned=len(hits))


def run_search(query: str, *, limit: int = 10) -> SearchResult:
    """Execute a live AOC search via AocClient.

    Uses WordPress's default `?s=<query>` search endpoint.
    """
    search_url = f"{config.AOC_BASE_URL}/?" + urlencode({"s": query})
    with AocClient() as client:
        response = client.get(search_url)
    return parse_search_results(response.text, limit=limit)
