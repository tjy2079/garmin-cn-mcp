"""Garmin CN (garmin.cn) login — generates MCP session via Playwright browser.

Usage:
    export GARMIN_EMAIL=you@example.com
    export GARMIN_PASSWORD=your_password
    python garmin_login.py

This opens a visible Chromium window to pass Cloudflare Turnstile,
logs into connect.garmin.cn, extracts cookies + CSRF token, and
saves them to ~/.garmin-connect-mcp/session.json for the MCP server.
"""
import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("GARMIN_EMAIL")
PASSWORD = os.environ.get("GARMIN_PASSWORD")

if not EMAIL or not PASSWORD:
    print("ERROR: Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables.")
    print("  export GARMIN_EMAIL=you@example.com")
    print("  export GARMIN_PASSWORD=your_password")
    sys.exit(1)

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()

        page.goto('https://connect.garmin.cn/app/activities', timeout=30000)

        for i in range(30):
            time.sleep(2)
            url = page.url
            if 'connect.garmin.cn/app' in url and 'sso' not in url:
                break
            if 'sso' in url and 'sign-in' in url:
                try:
                    page.wait_for_selector('input[type="email"]', timeout=30000)
                    page.fill('input[type="email"]', EMAIL)
                    page.fill('input[type="password"]', PASSWORD)
                    page.click('button[type="submit"]')
                except:
                    pass

        page.wait_for_timeout(3000)
        csrf = page.evaluate('() => document.querySelector("meta[name=csrf-token]")?.content ?? null')
        cookies = ctx.cookies()
        jwt = next((c['value'] for c in cookies if c['name'] == 'JWT_WEB'), None)

        if jwt and csrf:
            session = {
                'csrf_token': csrf,
                'cookies': [{'name': c['name'], 'value': c['value'], 'domain': c['domain']}
                           for c in cookies if 'garmin' in c.get('domain', '')]
            }
            p = Path.home() / '.garmin-connect-mcp' / 'session.json'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(session, indent=2))
            print(f'Saved: JWT={bool(jwt)}, CSRF={bool(csrf)}')
        else:
            print(f'Failed: JWT={bool(jwt)}, CSRF={bool(csrf)}')

        browser.close()

if __name__ == '__main__':
    login()
