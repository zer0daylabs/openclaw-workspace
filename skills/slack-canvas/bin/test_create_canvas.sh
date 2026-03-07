#!/bin/bash
# slack-canvas/bin/test_create_canvas.sh
# Test Canvas creation (creates a canvas and prints its ID)
# Usage: test_create_canvas.sh [channel_id]

source "$(dirname "$0")/_common.sh"
require_jq

CHANNEL_ID="${1:-C0AD1M21ZV0}"

log_info "Testing canvas creation in channel ${CHANNEL_ID}..."

PAYLOAD=$(jq -n --arg ch "$CHANNEL_ID" '{
    title: "Test Canvas - OpenClaw Skill",
    content: {type: "markdown", markdown: "# Test Canvas\n\nCreated by the `slack-canvas` skill.\n\n- **Status:** Working\n- **Timestamp:** \(now | floor | todate)\n\n_Delete this canvas when done testing._"},
    channel_id: $ch
}')

RESPONSE=$(slack_api "canvases.create" "$PAYLOAD" | assert_ok "Test canvas create")

CANVAS_ID=$(echo "$RESPONSE" | jq -r '.canvas_id // .id // empty')
log_info "Test canvas created: ${CANVAS_ID}"
echo ""
echo "To edit:   bin/canvas_edit.sh ${CANVAS_ID} insert_at_end '# More content'"
echo "To delete: bin/canvas_delete.sh ${CANVAS_ID}"
