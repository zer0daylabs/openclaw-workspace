#!/bin/bash
# Update Zer0Day Labs Agent Dashboard
# Should be called from heartbeat loop (~1 hour)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Source common utilities
source "$SCRIPT_DIR/../_common.sh" 2>/dev/null || true

# Canvas ID for the Agent Dashboard
CANVAS_ID="F0ALLTDTVFF"
CHANNEL="C0AD1M21ZV0"

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

# Count tasks by status
TASK_PENDING=$(bash "$BASE_DIR/skills/todo-management/scripts/todo.sh" entry list 2>/dev/null | grep -c "pending" || echo "0")
TASK_INPROG=$(bash "$BASE_DIR/skills/todo-management/scripts/todo.sh" entry list 2>/dev/null | grep -c "in_progress" || echo "0")
TASK_DONE=$(bash "$BASE_DIR/skills/todo-management/scripts/todo.sh" entry list 2>/dev/null | grep -c "done" || echo "0")

# Get current time for heartbeat tracking
HEARTBEAT_STATE="~/.openclaw/workspace/memory/heartbeat-state.json"
if [ -f "$HEARTBEAT_STATE" ]; then
    LAST_CHECKED=$(jq -r '.lastCheckTime // "never"' "$HEARTBEAT_STATE" 2>/dev/null || echo "never")
else
    LAST_CHECKED="never"
fi

# Update canvas with recent activity
UPDATE_CONTENT="## :update: Live Status (Updated: $TIMESTAMP)

**Tasks Today:**
- Pending: $TASK_PENDING
- In Progress: $TASK_INPROG
- Completed: $TASK_DONE

**Last Heartbeat:** $LAST_CHECKED

**Recent Updates:**
- 09:26 - MS 365 CLI setup initiated
- 03:50 - Infrastructure cleanup started

---
*Dashboard auto-updates every heartbeat (~1 hour)*
"

# Append to end of canvas
echo "Updating Agent Dashboard..."
bash "$SCRIPT_DIR/canvas_edit.sh" "$CANVAS_ID" "insert_at_end" "$UPDATE_CONTENT"

echo "✓ Dashboard updated: $CANVAS_ID"
