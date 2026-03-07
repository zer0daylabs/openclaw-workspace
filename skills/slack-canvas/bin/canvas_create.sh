#!/bin/bash
# slack-canvas/bin/canvas_create.sh
# Create a new Slack Canvas
# Usage: canvas_create.sh <title> [markdown_content] [channel_id]
#
# Examples:
#   canvas_create.sh "Project Status"
#   canvas_create.sh "Meeting Notes" "# Standup\n- Item 1\n- Item 2"
#   canvas_create.sh "Team Wiki" "# Docs" C0AD1M21ZV0

source "$(dirname "$0")/_common.sh"
require_jq

TITLE="${1:-}"
CONTENT="${2:-}"
CHANNEL_ID="${3:-}"

if [ -z "$TITLE" ]; then
    echo "Usage: $0 <title> [markdown_content] [channel_id]"
    exit 1
fi

# Convert content to proper JSON format with escaped newlines
if [ -n "$CONTENT" ]; then
    # Use jq to properly escape the markdown content
    CONTENT_JSON=$(echo "$CONTENT" | jq -Rs '.')
    PAYLOAD=$(jq -n \
        --arg title "$TITLE" \
        --argjson content "$CONTENT_JSON" \
        --arg channel "$CHANNEL_ID" \
        '{title: $title}
         + {document_content: {type: "markdown", markdown: $content}}
         + (if $channel != "" then {channel_id: $channel} else {} end)')
else
    PAYLOAD=$(jq -n \
        --arg title "$TITLE" \
        '{title: $title}')
fi

log_info "Creating canvas: ${TITLE}"

RESPONSE=$(slack_api "canvases.create" "$PAYLOAD" | assert_ok "Canvas create")

CANVAS_ID=$(echo "$RESPONSE" | jq -r '.canvas_id // .id // empty')
log_info "Canvas created: ${CANVAS_ID}"
echo "$RESPONSE" | jq '{ok, canvas_id: (.canvas_id // .id)}'
