#!/bin/bash
# Railway project rename helper script
# Generated: 2026-03-08 09:30 MST
# Purpose: Batch rename Railway projects to meaningful names

# Configuration
API_URL="https://railway.app/graph/ql"
AUTH_HEADER="Authorization: Bearer YOUR_TOKEN_HERE"  # Find token first

# Project ID mapping (from railway project list --json)
declare -A PROJECT_IDS
PROJECT_IDS["lucky-playfulness"]="dea04097-ee82-4f7a-9766-30fbe718ff72"
PROJECT_IDS["truthful-warmth"]="4b9635d2-aed0-4464-b6f5-b1386123ddd9"
PROJECT_IDS["appealing-laughter"]="3cafd6b5-75b8-4fa7-9ade-abe946180450"
PROJECT_IDS["audio-converter"]="561b9e81-07d2-4309-98dd-69a26deaa056"
PROJECT_IDS["user-data-subscriptions"]="11e814a5-cc83-4488-9564-e82322b56743"
PROJECT_IDS["new-db-app"]="e08a6f57-1e45-490b-8a5e-bfd1c6778ebb"
PROJECT_IDS["SlackBot"]="cef960ee-e2b9-467d-91e6-8328815436b8"

# New names
NEW_NAMES=("MusicGen-DB" "cleanup-target" "cleanup-target" "audio-converter" "user-data-subscriptions" "new-db-app" "SlackBot")

# Query each project and rename
rename_project() {
  local current_name=$1
  local new_name=$2
  local project_id=${PROJECT_IDS[$current_name]}
  
  if [[ -z "$project_id" ]]; then
    echo "❌ Unknown project: $current_name"
    return 1
  fi
  
  echo "Renaming $current_name → $new_name (ID: $project_id)"
  
  curl -s -X POST "$API_URL" \
    -H "$AUTH_HEADER" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"mutation { updateProject(id: \"$project_id\", name: \"$new_name\") { id name } }\"}"
}

# Batch rename
rename_project "lucky-playfulness" "MusicGen-DB"
rename_project "new-db-app" "AudioStudio-DB"  # Guess this is AudioStudio's DB

# Projects to keep as-is
# - truthful-warmth: unused, consider deletion
# - appealing-laughter: unused, consider deletion
# - audio-converter: functional
# - user-data-subscriptions: functional
# - SlackBot: functional

echo "\nNote: Find Railway token in ~/.railway/ or authenticate with 'railway whoami'"
