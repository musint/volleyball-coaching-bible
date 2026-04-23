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

from playwright.async_api import async_playwright

from aoc_mcp import config


async def run_login() -> int:
    """Open headed Chromium, wait for the user to log in, save session state."""
    from playwright.async_api import Error as PlaywrightError

    try:
        async with async_playwright() as p:
            # Prefer the user's real Chrome if available; fall back to Playwright's Chromium.
            # Cloudflare's bot detection trusts real Chrome far more than bundled Chromium.
            launch_args = [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
            try:
                browser = await p.chromium.launch(
                    headless=False,
                    channel="chrome",
                    args=launch_args,
                )
            except PlaywrightError:
                # channel="chrome" requires Google Chrome installed on the system.
                # Fall back to Playwright's bundled Chromium (less stealth but always available).
                print(
                    "[auth] Google Chrome not found; falling back to Playwright Chromium. "
                    "If Cloudflare blocks you, install Google Chrome and retry.",
                    file=sys.stderr,
                )
                try:
                    browser = await p.chromium.launch(
                        headless=False,
                        args=launch_args,
                    )
                except PlaywrightError as e:
                    print(
                        f"[auth] ERROR: failed to launch Chromium: {e}\n"
                        f"[auth] Did you run `playwright install chromium` inside the venv?",
                        file=sys.stderr,
                    )
                    return 1

            context = await browser.new_context(
                user_agent=config.USER_AGENT,
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                timezone_id="America/New_York",
            )
            # Stealth init: hide automation markers before any page loads.
            await context.add_init_script("""
                // Hide navigator.webdriver
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                // Fake window.chrome
                window.chrome = { runtime: {} };
                // Fake plugins (some sites check plugin count)
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                // Fake languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                // Hide permission query automation artifact
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications'
                        ? Promise.resolve({ state: Notification.permission })
                        : originalQuery(parameters)
                );
            """)
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
                print(
                    "[auth] ERROR: login timeout — no auth cookie observed.",
                    file=sys.stderr,
                )
                await browser.close()
                return 1

            try:
                config.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
                await context.storage_state(path=str(config.SESSION_FILE))
            except OSError as e:
                print(
                    f"[auth] ERROR: could not write session file {config.SESSION_FILE}: {e}",
                    file=sys.stderr,
                )
                await browser.close()
                return 1

            print(f"[auth] Authenticated. Session saved to {config.SESSION_FILE}")
            await browser.close()
            return 0
    except PlaywrightError as e:
        print(
            f"[auth] ERROR: Playwright runtime error: {e}",
            file=sys.stderr,
        )
        return 1


async def run_verify() -> int:
    """Load the saved session, hit a minimal AOC URL, check for login-form signal."""
    from aoc_mcp.client import AocClient
    from aoc_mcp.errors import SessionExpired, AocError
    import httpx

    try:
        with AocClient() as client:
            client.get(config.AOC_BASE_URL)
    except SessionExpired:
        print(
            "[auth] Session is EXPIRED or missing. "
            "Run `python -m aoc_mcp.auth` to re-auth.",
            file=sys.stderr,
        )
        return 1
    except (httpx.ConnectError, httpx.TimeoutException) as e:
        print(
            f"[auth] Network error, could not reach AOC: {e}",
            file=sys.stderr,
        )
        return 3
    except AocError as e:
        print(f"[auth] Unexpected error during verify: {e}", file=sys.stderr)
        return 2

    print("[auth] Session is VALID.")
    return 0


def run_import_from_browser(browser_name: str | None = None) -> int:
    """Import AOC cookies from the user's installed browser and save as .session.json.

    Uses browser_cookie3 to read Chrome/Firefox/Edge's local cookie store. Requires
    the user to have logged into AOC in that browser first. This path avoids
    Playwright's automation fingerprint entirely.
    """
    import json as _json

    try:
        import browser_cookie3
    except ImportError:
        print(
            "[auth] browser_cookie3 not installed. "
            "Run `pip install browser_cookie3` inside the venv.",
            file=sys.stderr,
        )
        return 1

    domain = "theartofcoachingvolleyball.com"

    loaders = {
        "chrome":  browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "edge":    browser_cookie3.edge,
        "brave":   browser_cookie3.brave,
    }

    if browser_name and browser_name in loaders:
        try:
            cj = loaders[browser_name](domain_name=domain)
        except Exception as e:
            print(f"[auth] Could not read {browser_name} cookies: {e}", file=sys.stderr)
            return 1
    elif browser_name:
        print(
            f"[auth] Unknown browser '{browser_name}'. "
            f"Choose from: {', '.join(loaders.keys())}",
            file=sys.stderr,
        )
        return 1
    else:
        # auto-detect: try `load()` which aggregates across browsers
        try:
            cj = browser_cookie3.load(domain_name=domain)
        except Exception as e:
            print(
                f"[auth] Auto-detect failed: {e}. "
                f"Try `--from-browser chrome` (or firefox/edge/brave) explicitly.",
                file=sys.stderr,
            )
            return 1

    cookies = []
    for c in cj:
        cookies.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "expires": c.expires if c.expires else -1,
        })

    if not cookies:
        print(
            f"[auth] No cookies found for {domain}. "
            "Make sure you've logged into AOC in the selected browser "
            "and that the browser is closed (or permits external read).",
            file=sys.stderr,
        )
        return 1

    has_wp_login = any(c["name"].startswith("wordpress_logged_in_") for c in cookies)
    if not has_wp_login:
        print(
            f"[auth] Warning: no `wordpress_logged_in_*` cookie found. "
            f"You may not be authenticated. Cookies captured anyway ({len(cookies)} total).",
            file=sys.stderr,
        )

    storage_state = {"cookies": cookies, "origins": []}
    config.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    config.SESSION_FILE.write_text(_json.dumps(storage_state, indent=2))
    print(f"[auth] Imported {len(cookies)} cookies from browser to {config.SESSION_FILE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="AOC auth CLI")
    parser.add_argument(
        "--verify", action="store_true",
        help="Only verify existing session; do not log in",
    )
    parser.add_argument(
        "--from-browser", metavar="BROWSER", nargs="?", const="auto",
        help="Import cookies from an installed browser instead of launching Playwright. "
             "Pass one of: chrome, firefox, edge, brave. With no arg, tries all.",
    )
    args = parser.parse_args()

    if args.verify:
        return asyncio.run(run_verify())
    if args.from_browser:
        name = None if args.from_browser == "auto" else args.from_browser
        return run_import_from_browser(name)
    return asyncio.run(run_login())


if __name__ == "__main__":
    sys.exit(main())
