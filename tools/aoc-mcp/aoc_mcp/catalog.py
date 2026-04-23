"""AOC category/topic listing.

Reuses parse_search_results from search.py since AOC's Genesis archive template
is shared between /?s=<query> search pages and /category/<slug>/ category pages.
Both render the same `article.post.entry` cards inside `div.archive-inner`.
"""
from __future__ import annotations

from aoc_mcp import config
from aoc_mcp.client import AocClient
from aoc_mcp.errors import UnknownTopic
from aoc_mcp.models import SearchResult
from aoc_mcp.search import parse_search_results

# Category pages reuse the same archive template as search; DOM is identical.
parse_category_page = parse_search_results


def list_recent(topic: str, *, limit: int = 20) -> SearchResult:
    """Fetch the most recent N items in an AOC topic category.

    Raises UnknownTopic if `topic` is not in config.KNOWN_TOPICS.
    """
    if topic not in config.KNOWN_TOPICS:
        raise UnknownTopic(
            topic=topic,
            known_topics=list(config.KNOWN_TOPICS.keys()),
        )
    _display_name, path = config.KNOWN_TOPICS[topic]
    url = config.AOC_BASE_URL + path
    with AocClient() as client:
        response = client.get(url)
    return parse_category_page(response.text, limit=limit)
