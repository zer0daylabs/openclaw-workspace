#!/usr/bin/env bash
set -euo pipefail

# heartbeat-state.sh — Manage heartbeat counter and cadence tracking
# Usage:
#   heartbeat-state.sh tick              — Increment counter, show due cadences
#   heartbeat-state.sh check <cadence>   — Check if a cadence is due
#   heartbeat-state.sh done <cadence>    — Mark a cadence as completed
#   heartbeat-state.sh stat <key> [+N]   — Increment a todayStats counter
#   heartbeat-state.sh show              — Show current state summary
#   heartbeat-state.sh error "<msg>"     — Log an error to error-journal.md

STATE_FILE="$HOME/.openclaw/workspace/memory/heartbeat-state.json"
ERROR_JOURNAL="$HOME/.openclaw/workspace/memory/error-journal.md"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "ERROR: $STATE_FILE not found"
  exit 1
fi

cmd="${1:-show}"

case "$cmd" in
  tick)
    # Increment heartbeat counter and update timestamp
    counter=$(jq '.heartbeatCounter' "$STATE_FILE")
    new_counter=$((counter + 1))
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    today=$(date +"%Y-%m-%d")

    # Reset daily stats if new day
    current_date=$(jq -r '.todayStats.date // ""' "$STATE_FILE")
    if [[ "$current_date" != "$today" ]]; then
      jq --arg d "$today" '.todayStats = {date: $d, tasksCompleted: 0, tasksSkipped: 0, tasksCreated: 0, errorsEncountered: 0, factsStored: 0, knowledgeFilesUpdated: 0}' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    fi

    # Update counter and timestamp
    jq --argjson c "$new_counter" --arg t "$now" '.heartbeatCounter = $c | .lastHeartbeat = $t' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

    echo "Heartbeat #$new_counter ($now)"

    # Check which cadences are due
    for cadence in $(jq -r '.cadences | keys[]' "$STATE_FILE"); do
      every=$(jq -r ".cadences[\"$cadence\"].every" "$STATE_FILE")
      last=$(jq -r ".cadences[\"$cadence\"].lastRun" "$STATE_FILE")
      desc=$(jq -r ".cadences[\"$cadence\"].description" "$STATE_FILE")
      since=$((new_counter - last))
      if [[ $since -ge $every ]]; then
        echo "  DUE: $cadence ($desc) — last run $since heartbeats ago"
      fi
    done
    ;;

  check)
    cadence="${2:?Usage: heartbeat-state.sh check <cadence>}"
    counter=$(jq '.heartbeatCounter' "$STATE_FILE")
    every=$(jq -r ".cadences[\"$cadence\"].every // 0" "$STATE_FILE")
    last=$(jq -r ".cadences[\"$cadence\"].lastRun // 0" "$STATE_FILE")
    since=$((counter - last))
    if [[ $every -eq 0 ]]; then
      echo "UNKNOWN cadence: $cadence"
      exit 1
    fi
    if [[ $since -ge $every ]]; then
      echo "DUE"
    else
      remaining=$((every - since))
      echo "NOT_DUE ($remaining heartbeats remaining)"
    fi
    ;;

  done)
    cadence="${2:?Usage: heartbeat-state.sh done <cadence>}"
    counter=$(jq '.heartbeatCounter' "$STATE_FILE")
    jq --arg c "$cadence" --argjson v "$counter" '.cadences[$c].lastRun = $v' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    echo "Marked $cadence done at heartbeat #$counter"
    ;;

  stat)
    key="${2:?Usage: heartbeat-state.sh stat <key> [+N]}"
    increment="${3:-+1}"
    increment="${increment#+}"
    jq --arg k "$key" --argjson v "$increment" '.todayStats[$k] = ((.todayStats[$k] // 0) + $v)' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    new_val=$(jq --arg k "$key" '.todayStats[$k]' "$STATE_FILE")
    echo "$key: $new_val"
    ;;

  error)
    msg="${2:?Usage: heartbeat-state.sh error \"<message>\"}"
    now=$(date +"%Y-%m-%d %H:%M:%S %Z")
    counter=$(jq '.heartbeatCounter' "$STATE_FILE")

    # Increment error counter
    jq '.todayStats.errorsEncountered = ((.todayStats.errorsEncountered // 0) + 1)' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

    # Create error journal if missing
    if [[ ! -f "$ERROR_JOURNAL" ]]; then
      cat > "$ERROR_JOURNAL" << 'HEADER'
# CB Error Journal

Errors encountered during autonomous operation. Use this to avoid repeating mistakes.

---

HEADER
    fi

    # Append error entry
    cat >> "$ERROR_JOURNAL" << EOF
### $now (heartbeat #$counter)
$msg

---

EOF
    echo "Error logged to $ERROR_JOURNAL"
    ;;

  show)
    counter=$(jq '.heartbeatCounter' "$STATE_FILE")
    last=$(jq -r '.lastHeartbeat // "never"' "$STATE_FILE")
    echo "=== Heartbeat State ==="
    echo "Counter: #$counter"
    echo "Last: $last"
    echo ""
    echo "=== Cadences ==="
    for cadence in $(jq -r '.cadences | keys[]' "$STATE_FILE"); do
      every=$(jq -r ".cadences[\"$cadence\"].every" "$STATE_FILE")
      last_run=$(jq -r ".cadences[\"$cadence\"].lastRun" "$STATE_FILE")
      desc=$(jq -r ".cadences[\"$cadence\"].description" "$STATE_FILE")
      since=$((counter - last_run))
      if [[ $since -ge $every ]]; then
        status="DUE"
      else
        remaining=$((every - since))
        status="in $remaining"
      fi
      printf "  %-20s every %-4s  [$status]  %s\n" "$cadence" "$every" "$desc"
    done
    echo ""
    echo "=== Today's Stats ==="
    jq -r '.todayStats | to_entries[] | "  \(.key): \(.value)"' "$STATE_FILE"
    ;;

  *)
    echo "Usage: heartbeat-state.sh {tick|check|done|stat|error|show}"
    exit 1
    ;;
esac
