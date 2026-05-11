# MyThesis — Garmin CN MCP Project

## Environment
- Python venv: `.venv`
- Proxy: Clash Verge on `127.0.0.1:7897`
- Node.js: v22 (global install at `%APPDATA%/npm/node_modules`)

## Garmin CN Data Access
- MCP server: `garmin-cn` (patched @etweisberg/garmin-connect-mcp)
- Login script: `python garmin_login.py` (needs `GARMIN_EMAIL` + `GARMIN_PASSWORD` env vars)
- Session check: `python check_session.py`
- Session stored at: `~/.garmin-connect-mcp/session.json`
- Session expires after a few hours — re-run `garmin_login.py` when data queries return 401.

## How it works
- Garmin CN (`garmin.cn`) blocks non-browser HTTP with Cloudflare WAF.
- The MCP server routes all API calls through a headless Chromium browser (Playwright).
- Login requires a visible browser (`headless=False`) to pass Cloudflare Turnstile.

## Athlete Profile
- 5K PB: 15:14 (Oct 2025, Xi'an)
- 10K PB: 31:48 (Oct 2025, Xi'an)
- Marathon: ~2:27 (Mar 2025, Wuxi)
