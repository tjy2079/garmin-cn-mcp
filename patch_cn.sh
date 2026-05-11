#!/bin/bash
# Patch @etweisberg/garmin-connect-mcp for Garmin China (garmin.cn)
# Replaces all hardcoded .com domains with .cn equivalents.
#
# Usage: bash patch_cn.sh

set -e

GLOBAL_DIR=$(npm root -g 2>/dev/null || echo "")
if [ -z "$GLOBAL_DIR" ]; then
    echo "ERROR: npm not found or no global modules."
    echo "Install the MCP server first: npm install -g @etweisberg/garmin-connect-mcp"
    exit 1
fi

DIST="$GLOBAL_DIR/@etweisberg/garmin-connect-mcp/dist"
if [ ! -d "$DIST" ]; then
    echo "ERROR: @etweisberg/garmin-connect-mcp not found at $DIST"
    echo "Install it: npm install -g @etweisberg/garmin-connect-mcp"
    exit 1
fi

echo "Patching $DIST ..."

sed -i 's/connect\.garmin\.com/connect.garmin.cn/g' "$DIST"/*.js
sed -i 's/sso\.garmin\.com/sso.garmin.cn/g'         "$DIST"/*.js
sed -i 's/connectapi\.garmin\.com/connectapi.garmin.cn/g' "$DIST"/*.js

echo "Done. MCP server patched for garmin.cn"
