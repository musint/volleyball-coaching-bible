# AOC MCP

Local MCP server exposing Art of Coaching Volleyball (paid-member) content as tools for Claude Code and other MCP clients. Part of the Volleyball Coaching Bible wiki project.

See `docs/superpowers/specs/2026-04-23-aoc-mcp-design.md` (in the parent repo) for the full design.

## Install

```bash
cd tools/aoc-mcp
python -m venv .venv
source .venv/Scripts/activate        # Windows bash; see README for cmd/PowerShell
pip install -e .[dev]
playwright install chromium
```

## First-time auth

```bash
python -m aoc_mcp.auth
```

Opens Chromium. Log into AOC manually. On success, `.session.json` is saved and the window closes.

## More

Run `pytest` to verify install. See parent project's spec for detail.
