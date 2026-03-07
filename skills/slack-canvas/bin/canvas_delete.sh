#!/bin/bash
# slack-canvas/bin/canvas_delete.sh
# Delete a Slack Canvas
# Usage: canvas_delete.sh <canvas_id>

source "$(dirname "$0")/_common.sh"
require_jq

CANVAS_ID="${1:-}"

if [ -z "$CANVAS_ID" ]; then
    echo "Usage: $0 <canvas_id>"
    exit 1
fi

PAYLOAD=$(jq -n --arg cid "$CANVAS_ID" '{canvas_id: $cid}')

log_warn "Deleting canvas: ${CANVAS_ID}"

slack_api "canvases.delete" "$PAYLOAD" | assert_ok "Canvas delete"

log_info "Canvas ${CANVAS_ID} deleted"
