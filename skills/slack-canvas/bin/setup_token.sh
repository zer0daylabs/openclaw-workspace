#!/bin/bash
# slack-canvas/bin/setup_token.sh
# Diagnose and display token resolution status
# The actual token resolution is handled by _common.sh (resolve_token)

source "$(dirname "$0")/_common.sh"

echo "=== Slack Canvas Token Setup ==="
echo ""

TOKEN=$(resolve_token 2>/dev/null) && {
    log_info "Token resolved (${TOKEN:0:15}...)"
    echo ""
    echo "Source priority:"
    echo "  1. SLACK_BOT_TOKEN env var"
    echo "  2. openclaw config channels.slack.botToken"
    echo "  3. openclaw password vault (slack/canvas-bot-token)"
    echo ""
    echo "Required OAuth scopes: canvases:write, canvases:read"
    echo "Run: bin/verify_scopes.sh to check"
} || {
    echo ""
    echo "To configure, choose one:"
    echo "  1. export SLACK_BOT_TOKEN='xoxb-...'"
    echo "  2. Token is auto-read from openclaw.json channels.slack.botToken"
    echo "  3. openclaw password set slack/canvas-bot-token 'xoxb-...'"
    echo ""
    echo "Required OAuth scopes: canvases:write, canvases:read"
    exit 1
}
