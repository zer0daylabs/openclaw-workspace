#!/bin/bash
# Graphiti Query Helper for Zer0Day Labs
# Usage: ./graphiti-query.sh "search query here"

set -e

GRAPHITI_URL="http://localhost:8001"

# Check if query provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"search query here\""
    exit 1
fi

QUERY="$1"

# Search graphiti using proper JSON encoding
RESPONSE=$(curl -s -X POST "$GRAPHITI_URL/search" \
  -H "Content-Type: application/json" \
  --data-binary "{\"query\": \"$QUERY\", \"group_ids\": [\"clawdbot-main\"], \"max_facts\": 10}")

# Extract and display facts
FACTS=$(echo "$RESPONSE" | jq -r '.facts[] | "• \(.fact)"')
COUNT=$(echo "$RESPONSE" | jq '.facts | length')

echo "📊 Found $COUNT relevant facts for query: \"$QUERY\""
echo ""
echo "$FACTS"
