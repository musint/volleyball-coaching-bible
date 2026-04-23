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

# Known topic slugs for aoc_list_recent.
# Maps our slug → (display name, AOC category URL path). Paths captured from live
# AOC inspection during Task 6. If AOC reorganizes its category tree, refresh by
# running `python -m aoc_mcp.discover` and re-scraping the category links.
KNOWN_TOPICS: dict[str, tuple[str, str]] = {
    # Skill-specific drill categories (under /category/drill/)
    "passing":            ("Passing Drills",             "/category/drill/passing-drills/"),
    "setting":            ("Setting Drills",             "/category/drill/setting-drills/"),
    "hitting":            ("Hitting Drills",             "/category/drill/hitting-drills/"),
    "blocking":           ("Blocking Drills",            "/category/drill/blocking-drills/"),
    "serving":            ("Serving Drills",             "/category/drill/serving-drills/"),
    "defense":            ("Individual Defense Drills",  "/category/drill/individual-defense-drills/"),
    "ball-control":       ("Ball Control Drills",        "/category/drill/ball-control-drills/"),
    "warm-up":            ("Warm-Up Drills",             "/category/drill/warm-up-2/"),
    "at-home":            ("At-Home Drills",             "/category/drill/at-home-drills/"),
    "small-group":        ("Small Group Drills",         "/category/drill/small-group-drills/"),
    "team-drills":        ("Team Drills",                "/category/drill/team-drills/"),
    # Systems & strategy (under /category/coaching-volleyball/)
    "offense":            ("Offense",                    "/category/coaching-volleyball/offense/"),
    "defensive-systems":  ("Defensive Systems",          "/category/coaching-volleyball/defensive-systems/"),
    "rotations":          ("Rotations",                  "/category/coaching-volleyball/rotations/"),
    "serve-receive":      ("Serve-Receive",              "/category/coaching-volleyball/serve-receive/"),
    "transitions":        ("Transitions",                "/category/coaching-volleyball/transitions/"),
    "out-of-system":      ("Out of System",              "/category/coaching-volleyball/out-of-system/"),
    "game-strategy":      ("Game Strategy",              "/category/coaching-volleyball/game-strategy/"),
    "practice-planning":  ("Practice",                   "/category/coaching-volleyball/practice/"),
    # Positions (under /category/positions/)
    "setter":             ("Setters",                    "/category/positions/setter/"),
    "libero":             ("Liberos",                    "/category/positions/libero/"),
    "outside-hitter":     ("Outside Hitters",            "/category/positions/outside-hitter/"),
    "middle-blocker":     ("Middle Blockers",            "/category/positions/middle-blocker/"),
    "opposite":           ("Opposites",                  "/category/positions/opposite-right-side-hitter/"),
    # Other
    "premium":            ("Premium",                    "/category/premium/"),
    "injury":             ("Injury Prevention",          "/category/injury/"),
    "sports-performance": ("Sports Performance",         "/category/health/sports-performance/"),
    "coach-connection":   ("Coach Connection",           "/category/coach-connection/"),
}

# Session-cookie names to detect during Playwright login. AOC uses the standard
# WordPress `wordpress_logged_in_<hash>` cookie; observed in IC1 with hash
# suffix "8414658413d848e50f94a6155f4f4ffe" for user mumumumagoo. Detection via
# startswith() in auth.py covers any hash, so this list stays empty for normal
# runs — add entries here only if AOC ever ships a non-WordPress auth signal.
AUTH_COOKIE_NAMES: list[str] = []
