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
