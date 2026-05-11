"""Quick check if Garmin CN session is still valid."""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_FILE = Path.home() / ".garmin-connect-mcp" / "session.json"


def check():
    if not SESSION_FILE.exists():
        print("NO_SESSION: Run garmin_login.py first.")
        sys.exit(1)

    data = json.loads(SESSION_FILE.read_text())
    cookies = data.get("cookies", [])
    jwt = any(c["name"] == "JWT_WEB" for c in cookies)

    if not jwt:
        print("EXPIRED: No JWT_WEB in session. Re-run garmin_login.py.")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        ctx.add_cookies(
            [{"name": c["name"], "value": c["value"],
              "domain": c["domain"], "path": "/"} for c in cookies]
        )
        page = ctx.new_page()

        resp = page.goto(
            "https://connect.garmin.cn/app/activities",
            timeout=20000,
            wait_until="domcontentloaded",
        )

        if "sso.garmin.cn" in page.url:
            print("EXPIRED: Session redirected to SSO. Re-run garmin_login.py.")
            browser.close()
            sys.exit(1)

        print("OK: Session is valid.")
        browser.close()


if __name__ == "__main__":
    check()
