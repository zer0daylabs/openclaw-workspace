#!/usr/bin/env bash
# Simple search script for telecom knowledge vault
# Usage: search-kb.sh "query"

set -euo pipefail

VAULT_PATH="${VAULT_PATH:-~/.openclaw/workspace/telecom-kb/vault}"
QUERY="${1:?Usage: search-kb.sh \"query\"}"

# Find relevant files
echo "Searching for: $QUERY"
echo "==================="
echo ""

# Search in all markdown files
result=$(rg "$QUERY" --files-with-matches --glob "*.md" "$VAULT_PATH" 2>/dev/null || echo "")

if [ -z "$result" ]; then
    echo "No matches found for: $QUERY"
    exit 0
fi

# Print results with context
for file in $result; do
    filename=$(basename "$file")
    echo "📄 $filename"
    echo "------------------"
    rg --context 2 "$QUERY" "$file" | grep -v "^--$" | head -20
    echo ""
done
