"""Patch @etweisberg/garmin-connect-mcp for Garmin China (garmin.cn).
Cross-platform (Windows/Mac/Linux). Run after `npm install -g`.

Usage: python patch_cn.py
"""
import sys
import shutil
from pathlib import Path


def find_global_npm():
    """Find npm global node_modules directory."""
    candidates = [
        Path.home() / "AppData" / "Roaming" / "npm" / "node_modules",        # Windows
        Path("/usr/local/lib/node_modules"),                                   # macOS
        Path("/usr/lib/node_modules"),                                         # Linux
    ]
    for c in candidates:
        if c.exists():
            return c
    # Try npm itself
    import subprocess
    try:
        result = subprocess.run(
            ["npm", "root", "-g"], capture_output=True, text=True
        )
        return Path(result.stdout.strip())
    except Exception:
        return None


REPLACEMENTS = {
    "connect.garmin.com": "connect.garmin.cn",
    "sso.garmin.com": "sso.garmin.cn",
    "connectapi.garmin.com": "connectapi.garmin.cn",
}


def patch_dist(dist_dir: Path) -> int:
    """Replace .com domains with .cn equivalents in all JS files."""
    count = 0
    for js_file in dist_dir.glob("*.js"):
        text = js_file.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)
        if text != original:
            js_file.write_text(text, encoding="utf-8")
            count += 1
            print(f"  Patched: {js_file.name}")
    return count


def main():
    npm_root = find_global_npm()
    if not npm_root:
        print("ERROR: Could not find npm global node_modules.")
        print("Install the MCP server first:")
        print("  npm install -g @etweisberg/garmin-connect-mcp")
        sys.exit(1)

    dist = npm_root / "@etweisberg" / "garmin-connect-mcp" / "dist"
    if not dist.is_dir():
        print(f"ERROR: {dist} not found.")
        print("Install: npm install -g @etweisberg/garmin-connect-mcp")
        sys.exit(1)

    print(f"Patching: {dist}")
    n = patch_dist(dist)
    print(f"Done: {n} file(s) patched for garmin.cn")


if __name__ == "__main__":
    main()
