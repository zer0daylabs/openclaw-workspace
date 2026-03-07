#!/bin/bash
# slack-canvas/bin/_common.sh
# Shared helpers for slack-canvas skill scripts
# Source this file: source "$(dirname "$0")/_common.sh"

set -euo pipefail

# Colors (only when stdout is a terminal)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' NC=''
fi

log_info()  { echo -e "${GREEN}✓${NC} $1"; }
log_warn()  { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1" >&2; }

# Resolve the Slack bot token from (in order):
#   1. SLACK_BOT_TOKEN env var
#   2. OpenClaw config (channels.slack.botToken)
#   3. openclaw password vault
resolve_token() {
    # 1. Environment variable
    if [ -n "${SLACK_BOT_TOKEN:-}" ]; then
        echo "$SLACK_BOT_TOKEN"
        return 0
    fi

    # 2. OpenClaw config file — read botToken directly (CLI redacts secrets)
    local config_file="${HOME}/.openclaw/openclaw.json"
    if [ -f "$config_file" ] && command -v jq &>/dev/null; then
        local cfg_token
        cfg_token=$(jq -r '.channels.slack.botToken // empty' "$config_file" 2>/dev/null || true)
        if [ -n "$cfg_token" ] && [[ "$cfg_token" == xoxb-* ]]; then
            echo "$cfg_token"
            return 0
        fi
    fi

    # 3. Password vault
    if command -v openclaw &>/dev/null; then
        local vault_token
        vault_token=$(openclaw password get slack/canvas-bot-token 2>/dev/null || true)
        if [ -n "$vault_token" ]; then
            echo "$vault_token"
            return 0
        fi
    fi

    log_error "No Slack bot token found!"
    echo "Configure one of:" >&2
    echo "  1. export SLACK_BOT_TOKEN='xoxb-...'" >&2
    echo "  2. OpenClaw config channels.slack.botToken (already there if Slack is set up)" >&2
    echo "  3. openclaw password set slack/canvas-bot-token 'xoxb-...'" >&2
    return 1
}

# Require jq
require_jq() {
    if ! command -v jq &>/dev/null; then
        log_error "jq is required but not installed. Install with: sudo apt-get install jq"
        exit 1
    fi
}

# Call a Slack API method. Prints raw JSON response.
# Usage: slack_api <method> <json_payload>
slack_api() {
    local method="$1"
    local payload="$2"
    local token
    token=$(resolve_token)

    curl -sf -X POST \
        "https://slack.com/api/${method}" \
        -H "Authorization: Bearer ${token}" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "$payload" 2>/dev/null || {
            log_error "HTTP request to slack.com/api/${method} failed"
            return 1
        }
}

# Check a Slack API JSON response for ok:true, exit 1 on failure.
# Usage: echo "$response" | assert_ok "action description"
assert_ok() {
    local desc="${1:-API call}"
    local resp
    resp=$(cat)

    if echo "$resp" | jq -e '.ok == true' &>/dev/null; then
        echo "$resp"
        return 0
    else
        local err
        err=$(echo "$resp" | jq -r '.error // "unknown_error"' 2>/dev/null || echo "unknown_error")
        log_error "${desc} failed: ${err}"
        echo "$resp" | jq '.' 2>/dev/null || echo "$resp" >&2
        return 1
    fi
}
