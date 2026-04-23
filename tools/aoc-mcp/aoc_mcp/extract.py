"""Parse AOC article HTML into ArticleResult.

Selectors are captured from the live AOC fixture. If AOC updates its theme/DOM,
update these SELECTORS constants and re-run extract tests.

AOC runs WordPress with a Genesis child theme (`coaching_vb`). The post-page
structure is roughly:

    main.content
      └─ article.post.entry
           ├─ header.entry-header   (title, author, team, playlist/follow UI)
           ├─ div.entry-content     (the post body — may be very short for
           │                        video-backed Premium articles)
           └─ footer.entry-footer   (date, categories, hide/show toggle)

A parent `<div class="single-loop">` wraps the article + the right-hand
`<aside class="sidebar">` (Related/Recent content widget). For ingest we want
the full post wrapper so short video posts still surface author, categories,
and related-content context as markdown.
"""
from __future__ import annotations

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from aoc_mcp.errors import ParserFailed
from aoc_mcp.models import ArticleResult

# Selectors — confirmed against the live
# `live-article-kiraly-4-keys-forearm-pass.html` fixture.
SELECTOR_TITLE = "h1.entry-title"

# Body: prefer the Genesis `.single-loop` wrapper because the `entry-content`
# body can be tiny on video-backed Premium posts. Fall back to `article` then
# to `div.entry-content` for other themes / robustness.
SELECTOR_BODY = "div.single-loop, article.entry, article, div.entry-content"

# AOC uses <span class="entry-authorname"><a><h5>Name</h5></a></span>
SELECTOR_AUTHOR = (
    ".entry-authorname a, .author.vcard a, .byline .author, .entry-meta .author"
)
SELECTOR_DATE_META = 'meta[property="article:published_time"]'

# AOC uses <span class="entry-categories"><a rel="category tag">...</a></span>.
# Fall back to generic WP category/tag link patterns.
SELECTOR_TAGS = (
    ".entry-categories a, .entry-tags a, .cat-links a, "
    "a[rel~='category'], a[rel~='tag']"
)

# Site chrome to strip from the body BEFORE markdown conversion. We
# intentionally do NOT strip `<header>` / `<footer>` because the Genesis theme
# uses `<header class="entry-header">` and `<footer class="entry-footer">` to
# hold the article's title/author/date/categories — legitimate content we
# want in the markdown. We DO strip the site-level `<nav>` and sitewide
# `.site-header` / `.site-footer` chrome.
STRIP_SELECTORS = [
    "script",
    "style",
    "noscript",
    "nav",
    ".site-header",
    ".site-footer",
    ".site-subheader",
    ".ubernavbar",
    ".menu-primary",
    ".sharedaddy",           # Jetpack share buttons
    ".jp-relatedposts",      # Jetpack related posts
    ".shareaholic-canvas",   # Shareaholic embed placeholders
    ".author-box",
    ".follow-author",
    ".hideshow-btn",
    ".videoActions",
    ".post-navigation",
    ".comments-area",
    "form",
    # Pop-ups / modal overlays (AOC uses Popup Maker)
    ".pum-overlay",
    ".popmake-overlay",
    "[id^=pum-]",
    "[id^=popmake-]",
]


def _strip_chrome(element) -> None:
    """Decompose non-article chrome inside `element` in-place."""
    for sel in STRIP_SELECTORS:
        for junk in element.select(sel):
            junk.decompose()


def _collapse_blank_lines(text: str) -> str:
    """Collapse 3+ consecutive blank lines to 1."""
    lines: list[str] = []
    blank_run = 0
    for line in text.splitlines():
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                lines.append("")
        else:
            blank_run = 0
            lines.append(line)
    return "\n".join(lines).strip()


def parse_article(html: str, *, url: str) -> ArticleResult:
    """Parse AOC article HTML → ArticleResult.

    Raises:
        ParserFailed: if the title or body selectors match nothing.
    """
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one(SELECTOR_TITLE)
    body_el = soup.select_one(SELECTOR_BODY)

    if not title_el or not body_el:
        raise ParserFailed(url=url, snippet=html[:500])

    title = title_el.get_text(strip=True)

    # Extract author/date/tags from the full soup BEFORE we mutate the body,
    # so chrome stripping doesn't remove the selectors we care about.
    author_el = soup.select_one(SELECTOR_AUTHOR)
    author = author_el.get_text(strip=True) if author_el else None

    date_meta = soup.select_one(SELECTOR_DATE_META)
    date = None
    if date_meta and date_meta.get("content"):
        # ISO-8601 — keep YYYY-MM-DD prefix.
        date = date_meta["content"][:10]

    tag_els = soup.select(SELECTOR_TAGS)
    seen: set[str] = set()
    tags: list[str] = []
    for t in tag_els:
        text = t.get_text(strip=True)
        if text and text not in seen:
            seen.add(text)
            tags.append(text)

    # Strip chrome from the body before markdown conversion.
    _strip_chrome(body_el)

    body_html = str(body_el)
    markdown_text = md(body_html, heading_style="ATX").strip()
    markdown_text = _collapse_blank_lines(markdown_text)

    word_count = len(markdown_text.split())

    return ArticleResult(
        title=title,
        author=author,
        date=date,
        tags=tags,
        markdown=markdown_text,
        word_count=word_count,
        url=url,
    )
