"""Shared pydantic models for MCP tool return values."""
from pydantic import BaseModel, Field


class ArticleResult(BaseModel):
    title: str
    author: str | None = None
    date: str | None = None       # ISO-8601 YYYY-MM-DD if parseable, else None
    tags: list[str] = Field(default_factory=list)
    markdown: str
    word_count: int
    url: str


class SearchHit(BaseModel):
    title: str
    url: str
    author: str | None = None
    snippet: str = ""
    date: str | None = None


class SearchResult(BaseModel):
    hits: list[SearchHit]
    total_returned: int


class VideoResult(BaseModel):
    title: str
    author: str | None = None
    duration_sec: int | None = None
    transcript: str | None = None
    captions_source: str = "unavailable"  # vimeo|wistia|unavailable|unsupported_provider
    embed_url: str | None = None
    url: str
