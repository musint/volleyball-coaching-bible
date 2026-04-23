"""Playwright headed-login CLI for AOC.

Usage:
    python -m aoc_mcp.auth           # login mode: opens headed Chromium
    python -m aoc_mcp.auth --verify  # checks if existing session is valid
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

from aoc_mcp import config


async def run_login() -> int:
    """Open headed Chromium, wait for the user to log in, save session state."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=config.USER_AGENT)
        page = await context.new_page()

        print(f"[auth] Opening {config.AOC_LOGIN_URL} ...")
        await page.goto(config.AOC_LOGIN_URL)
        print(
            f"[auth] Please log into AOC in the opened browser window.\n"
            f"[auth] You have {config.AUTH_LOGIN_TIMEOUT_S // 60} minutes.\n"
            f"[auth] Waiting for login-completion signal..."
        )

        deadline = time.monotonic() + config.AUTH_LOGIN_TIMEOUT_S
        logged_in = False
        while time.monotonic() < deadline:
            await asyncio.sleep(2.0)
            cookies = await context.cookies()
            # Primary signal: cookie with name starting "wordpress_logged_in_"
            # (WordPress convention) OR any cookie matching the configured list.
            for c in cookies:
                name = c.get("name", "")
                if name.startswith("wordpress_logged_in_") or (
                    config.AUTH_COOKIE_NAMES
                    and name in config.AUTH_COOKIE_NAMES
                ):
                    logged_in = True
                    break
            if logged_in:
                break

        if not logged_in:
            print("[auth] ERROR: login timeout — no auth cookie observed.", file=sys.stderr)
            await browser.close()
            return 1

        config.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(config.SESSION_FILE))
        print(f"[auth] Authenticated. Session saved to {config.SESSION_FILE}")
        await browser.close()
        return 0


async def run_verify() -> int:
    """Load the saved session, hit a minimal AOC URL, check for login-form signal."""
    from aoc_mcp.client import AocClient
    from aoc_mcp.errors import SessionExpired, AocError

    try:
        client = AocClient()
    except SessionExpired:
        print("[auth] Session file missing or malformed.", file=sys.stderr)
        return 1

    try:
        client.get(config.AOC_BASE_URL)
    except SessionExpired:
        print("[auth] Session is EXPIRED. Run `python -m aoc_mcp.auth` to re-auth.")
        return 1
    except AocError as e:
        print(f"[auth] Unexpected error during verify: {e}", file=sys.stderr)
        return 2

    print("[auth] Session is VALID.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="AOC auth CLI")
    parser.add_argument("--verify", action="store_true",
                        help="Only verify existing session; do not log in")
    args = parser.parse_args()
    coro = run_verify() if args.verify else run_login()
    return asyncio.run(coro)


if __name__ == "__main__":
    sys.exit(main())
