"""MCP server entry point — stdio transport, registers 4 tools."""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

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
    payload: dict[str, Any] = {"code": err.code, "message": str(err)}
    for attr in ("url", "snippet", "topic", "known_topics", "provider", "status"):
        if hasattr(err, attr):
            payload[attr] = getattr(err, attr)
    return payload


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
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
