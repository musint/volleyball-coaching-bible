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

# Default seed: (slug, url). Slug becomes the filename under tests/fixtures/: <slug>.html
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
        "live-category-passing-drills",
        "https://www.theartofcoachingvolleyball.com/category/drill/passing-drills/",
    ),
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
