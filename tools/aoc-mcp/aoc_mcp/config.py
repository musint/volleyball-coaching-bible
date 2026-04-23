"""Configuration constants for the AOC MCP server.

No logic — only constants. Anything that needs to be tuned goes here so other
modules don't hard-code magic values.
"""
from pathlib import Path

# AOC site
AOC_BASE_URL = "https://www.theartofcoachingvolleyball.com"
AOC_LOGIN_URL = f"{AOC_BASE_URL}/login"

# User-Agent: a recent Chrome UA. Update manually when it ages. Matching the UA
# used during headed login (Playwright-Chromium) reduces fingerprint mismatch.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Session storage (gitignored)
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SESSION_FILE = PACKAGE_ROOT / ".session.json"
FIXTURES_DIR = PACKAGE_ROOT / "tests" / "fixtures"

# HTTP behavior
DEFAULT_TIMEOUT_S = 30.0
REQUEST_MIN_INTERVAL_S = 1.0   # rate limit: min spacing between requests
RETRY_429_BACKOFF_S = 1.0
RETRY_5XX_BACKOFF_S = 4.0

# Auth timeout
AUTH_LOGIN_TIMEOUT_S = 300     # user has 5 minutes to log in manually

# Known topic slugs for aoc_list_recent (extended during discovery; see Task 6)
# Maps our slug → (display name, AOC category URL path).
KNOWN_TOPICS: dict[str, tuple[str, str]] = {
    # populated in Task 6 from live AOC inspection
}

# Session-cookie names to detect during Playwright login. Populated in Task 5.
AUTH_COOKIE_NAMES: list[str] = [
    # populated in Task 5 after observing the real login flow
]
