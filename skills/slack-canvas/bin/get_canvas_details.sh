#!/bin/bash
# slack-canvas/bin/get_canvas_details.sh
# Get details of canvases in a channel
# Usage: get_canvas_details.sh [channel_id] [title_filter]

source "$(dirname "$0")/_common.sh"
require_jq

CHANNEL_ID="${1:-C0AD1M21ZV0}"
TITLE_FILTER="${2:-}"

PAYLOAD=$(jq -n --arg ch "$CHANNEL_ID" '{channel: $ch, types: "spaces", count: 20}')

RESPONSE=$(slack_api "files.list" "$PAYLOAD" | assert_ok "Get canvas details")

if [ -n "$TITLE_FILTER" ]; then
    echo "$RESPONSE" | jq -r --arg f "$TITLE_FILTER" \
        '.files[] | select(.title | test($f; "i")) | "ID:      \(.id)\nTitle:   \(.title)\nCreated: \(.created // 0 | todate)\n"'
else
    echo "$RESPONSE" | jq -r \
        '.files[] | "ID:      \(.id)\nTitle:   \(.title // "untitled")\nCreated: \(.created // 0 | todate)\n"'
fi
