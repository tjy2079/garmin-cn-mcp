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
- 5K PB: 15:14 (2025-10-28, track, Xi'an)
- 10K PB: 31:48 (2025-10-26, track, Xi'an)
- Marathon: 2:27:20 (2025-03-23, Wuxi)
- VO2Max: 71
- Weight: 65kg, Height: 175cm
- Birth: 2004-07-01
- Location: Xi'an, China
- Garmin device: 3427042293
