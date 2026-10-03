#!/bin/bash
# Prepare the vendored Claude SEO plugin in Claude Code cloud sessions:
# write the Google service-account key from the environment and make sure
# the plugin's Python runtime and the DataForSEO MCP package are present.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

SEO_DIR="$CLAUDE_PROJECT_DIR/vendor/seo"
CONFIG_DIR="$HOME/.config/claude-seo"

# Google service account: GOOGLE_SA_KEY_B64 holds the base64-encoded JSON key.
if [ -n "${GOOGLE_SA_KEY_B64:-}" ]; then
  key_path="${GOOGLE_APPLICATION_CREDENTIALS:-$CONFIG_DIR/service_account.json}"
  mkdir -p "$(dirname "$key_path")"
  (umask 077; printf '%s' "$GOOGLE_SA_KEY_B64" | base64 -d > "$key_path.tmp")
  mv "$key_path.tmp" "$key_path"
  chmod 600 "$key_path"
fi

# Claude SEO runtime (isolated venv); skip the Chromium download.
if ! "$SEO_DIR/scripts/claude-seo" doctor >/dev/null 2>&1; then
  "$SEO_DIR/scripts/claude-seo" setup --skip-browser
fi

# Pre-fetch the DataForSEO MCP server used by .mcp.json.
if [ -n "${DATAFORSEO_USERNAME:-}" ]; then
  npx --yes --package=dataforseo-mcp-server@2.8.10 -- node -e "" >/dev/null 2>&1 || true
fi
