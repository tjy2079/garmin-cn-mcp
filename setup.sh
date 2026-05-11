#!/bin/bash
# One-shot setup: Garmin CN MCP server for Claude Code
# Prerequisites: Node.js 18+, Python 3.10+, npm
set -e

echo "============================================"
echo "  Garmin CN MCP Server Setup"
echo "============================================"

# 1. Install Node deps
echo ""
echo "[1/5] Installing MCP server..."
npm install -g @etweisberg/garmin-connect-mcp

# 2. Install Playwright browser
echo ""
echo "[2/5] Installing Chromium for Playwright..."
npx playwright install chromium

# 3. Patch for garmin.cn
echo ""
echo "[3/5] Patching for Garmin China..."
python3 patch_cn.py || python patch_cn.py

# 4. Install Python deps
echo ""
echo "[4/5] Installing Python dependencies..."
pip install playwright

# 5. Register with Claude Code
echo ""
echo "[5/5] Registering MCP server with Claude Code..."
GLOBAL_DIST=$(npm root -g)/@etweisberg/garmin-connect-mcp/dist
claude mcp add garmin-cn -- node "$GLOBAL_DIST/index.js"

echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Set your credentials:"
echo "     export GARMIN_EMAIL=you@example.com"
echo "     export GARMIN_PASSWORD=your_password"
echo ""
echo "  2. Log in (opens browser):"
echo "     python garmin_login.py"
echo ""
echo "  3. Verify:"
echo "     python check_session.py"
echo ""
echo "  4. Try in Claude Code:"
echo "     '查我最近的跑步数据'"
