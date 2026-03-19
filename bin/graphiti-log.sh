#!/bin/bash
# Graphiti Logging Helper for Zer0Day Labs
# Usage: ./graphiti-log.sh "Lesson: Write files immediately"
#        ./graphiti-log.sh "Decision: Memory system implemented"
#        ./graphiti-log.sh "Milestone: Graphiti operational"

set -e

GRAPHITI_URL="http://localhost:8001"
GROUP_ID="clawdbot-main"

# Check if message provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"Lesson/Decision/Milestone: Description\""
    exit 1
fi

MESSAGE="$1"

# Log to graphiti using proper JSON encoding
RESPONSE=$(curl -s -X POST "$GRAPHITI_URL/messages" \
  -H "Content-Type: application/json" \
  --data-binary "{\"group_id\": \"$GROUP_ID\", \"messages\": [{\"role\": \"user\", \"role_type\": \"user\", \"content\": \"$MESSAGE\"}]}")

if echo "$RESPONSE" | grep -q '"success"[: ]*true'; then
    echo "✅ Logged to Graphiti: $MESSAGE"
else
    echo "❌ Failed to log: $RESPONSE"
    exit 1
fi
