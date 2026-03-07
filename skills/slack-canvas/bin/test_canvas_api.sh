#!/bin/bash
# slack-canvas/bin/test_canvas_api.sh
# Quick smoke test: authenticate and try a canvas create/delete round-trip
# Usage: test_canvas_api.sh [channel_id]

source "$(dirname "$0")/_common.sh"
require_jq

CHANNEL_ID="${1:-C0AD1M21ZV0}"

echo "=== Slack Canvas API Smoke Test ==="
echo ""

# 1. Auth check
log_info "Step 1: Authenticating..."
AUTH=$(slack_api "auth.test" '{}' | assert_ok "auth.test")
BOT=$(echo "$AUTH" | jq -r '.user // "unknown"')
TEAM=$(echo "$AUTH" | jq -r '.team // "unknown"')
log_info "Authenticated as ${BOT} @ ${TEAM}"

# 2. Create a test canvas
log_info "Step 2: Creating test canvas..."
CREATE_PAYLOAD=$(jq -n --arg ch "$CHANNEL_ID" '{
    title: "slack-canvas smoke test",
    content: {type: "markdown", markdown: "# Smoke Test\n\nThis canvas was created by `test_canvas_api.sh`.\nIf you see this, the Canvas API is working.\n\nTimestamp: \(now | floor | todate)"},
    channel_id: $ch
}')
CREATE_RESP=$(slack_api "canvases.create" "$CREATE_PAYLOAD" | assert_ok "canvases.create")
CANVAS_ID=$(echo "$CREATE_RESP" | jq -r '.canvas_id // .id // empty')
log_info "Created canvas: ${CANVAS_ID}"

# 3. Edit the canvas
log_info "Step 3: Editing canvas (append)..."
EDIT_PAYLOAD=$(jq -n --arg cid "$CANVAS_ID" '{
    canvas_id: $cid,
    changes: [{operation: "insert_at_end", document_content: {type: "markdown", markdown: "\n---\n_Edit test passed._"}}]
}')
slack_api "canvases.edit" "$EDIT_PAYLOAD" | assert_ok "canvases.edit" >/dev/null
log_info "Edit successful"

# 4. Delete the test canvas
log_info "Step 4: Cleaning up (delete)..."
DEL_PAYLOAD=$(jq -n --arg cid "$CANVAS_ID" '{canvas_id: $cid}')
slack_api "canvases.delete" "$DEL_PAYLOAD" | assert_ok "canvases.delete" >/dev/null
log_info "Deleted test canvas"

echo ""
log_info "All tests passed! Canvas API is fully operational."
