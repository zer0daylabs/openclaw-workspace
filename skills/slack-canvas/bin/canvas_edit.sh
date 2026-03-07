#!/bin/bash
# slack-canvas/bin/canvas_edit.sh
# Edit an existing Slack Canvas
# Usage: canvas_edit.sh <canvas_id> <operation> <content> [section_id]
#
# Operations:
#   insert_at_end    - Append content
#   insert_at_start  - Prepend content
#   insert_after     - Insert after section (requires section_id)
#   insert_before    - Insert before section (requires section_id)
#   replace          - Replace canvas or section content
#   rename           - Rename canvas title
#
# Examples:
#   canvas_edit.sh F12345678 insert_at_end "# New Section\n- Item 1"
#   canvas_edit.sh F12345678 rename "Updated Title"
#   canvas_edit.sh F12345678 insert_after "- New item" temp:C:section123

source "$(dirname "$0")/_common.sh"
require_jq

CANVAS_ID="${1:-}"
OPERATION="${2:-}"
CONTENT="${3:-}"
SECTION_ID="${4:-}"

if [ -z "$CANVAS_ID" ] || [ -z "$OPERATION" ]; then
    echo "Usage: $0 <canvas_id> <operation> <content> [section_id]"
    echo ""
    echo "Operations: insert_at_end, insert_at_start, insert_after,"
    echo "            insert_before, replace, rename"
    exit 1
fi

# Build the change object with jq for safe JSON encoding
if [ "$OPERATION" = "rename" ]; then
    CHANGE=$(jq -n \
        --arg op "$OPERATION" \
        --arg content "$CONTENT" \
        '{operation: $op, title_content: {type: "markdown", markdown: $content}}')
elif [ -n "$SECTION_ID" ]; then
    CHANGE=$(jq -n \
        --arg op "$OPERATION" \
        --arg content "$CONTENT" \
        --arg section "$SECTION_ID" \
        '{operation: $op, section_id: $section, document_content: {type: "markdown", markdown: $content}}')
else
    CHANGE=$(jq -n \
        --arg op "$OPERATION" \
        --arg content "$CONTENT" \
        '{operation: $op, document_content: {type: "markdown", markdown: $content}}')
fi

PAYLOAD=$(jq -n --arg cid "$CANVAS_ID" --argjson change "$CHANGE" \
    '{canvas_id: $cid, changes: [$change]}')

log_info "Editing canvas ${CANVAS_ID} (${OPERATION})"

slack_api "canvases.edit" "$PAYLOAD" | assert_ok "Canvas edit"
