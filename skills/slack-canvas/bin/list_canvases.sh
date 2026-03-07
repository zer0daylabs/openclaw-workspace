#!/bin/bash
# slack-canvas/bin/list_canvases.sh
# List canvases in a Slack channel
# Usage: list_canvases.sh [channel_id] [limit]

source "$(dirname "$0")/_common.sh"
require_jq

CHANNEL_ID="${1:-C0AD1M21ZV0}"
LIMIT="${2:-20}"

PAYLOAD=$(jq -n \
    --arg ch "$CHANNEL_ID" \
    --argjson limit "$LIMIT" \
    '{channel: $ch, types: "spaces", count: $limit}')

log_info "Listing canvases in channel ${CHANNEL_ID}..."

RESPONSE=$(slack_api "files.list" "$PAYLOAD" | assert_ok "List canvases")

echo "$RESPONSE" | jq -r '.files[] | "\(.id)\t\(.title // "untitled")\t\(.created // 0 | todate)"' 2>/dev/null | column -t -s $'\t' || echo "No canvases found."
