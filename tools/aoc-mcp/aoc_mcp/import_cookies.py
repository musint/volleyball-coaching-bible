"""Convert a Cookie-Editor JSON export into the Playwright storage_state
session file the AOC MCP reads.

Escape hatch for when the headed login (auth.py) is blocked by Cloudflare
Turnstile: log into AOC in a normal browser, export cookies with the
Cookie-Editor extension (Export -> JSON), then run:

    python -m aoc_mcp.import_cookies <path-to-export.json>

Writes config.SESSION_FILE. Verify afterwards with:

    python -m aoc_mcp.auth --verify
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from aoc_mcp import config

SAMESITE_MAP = {
    "strict": "Strict",
    "lax": "Lax",
    "no_restriction": "None",
    "none": "None",
    "unspecified": "Lax",
    "": "Lax",
}


def convert(export_path: Path) -> int:
    try:
        raw = json.loads(export_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[import] ERROR: cannot read {export_path}: {e}", file=sys.stderr)
        return 1

    if isinstance(raw, dict) and "cookies" in raw:
        raw = raw["cookies"]
    if not isinstance(raw, list) or not raw:
        print("[import] ERROR: export is not a non-empty cookie list.", file=sys.stderr)
        return 1

    cookies = []
    seen_login = False
    for c in raw:
        name = c.get("name", "")
        if not name:
            continue
        if name.startswith("wordpress_logged_in_"):
            seen_login = True
        expires = c.get("expirationDate")
        cookies.append({
            "name": name,
            "value": c.get("value", ""),
            "domain": c.get("domain", ".theartofcoachingvolleyball.com"),
            "path": c.get("path", "/"),
            "expires": float(expires) if expires else -1,
            "httpOnly": bool(c.get("httpOnly", False)),
            "secure": bool(c.get("secure", True)),
            "sameSite": SAMESITE_MAP.get(str(c.get("sameSite", "")).lower(), "Lax"),
        })

    if not seen_login:
        print(
            "[import] WARNING: no wordpress_logged_in_* cookie in the export. "
            "Make sure you exported while logged in, from the AOC tab.",
            file=sys.stderr,
        )

    state = {"cookies": cookies, "origins": []}
    config.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    config.SESSION_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"[import] Wrote {len(cookies)} cookies to {config.SESSION_FILE}"
          + (" (login cookie present)" if seen_login else ""))
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    return convert(Path(sys.argv[1]))


if __name__ == "__main__":
    sys.exit(main())
