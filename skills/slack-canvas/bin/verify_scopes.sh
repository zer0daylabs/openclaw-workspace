#!/bin/bash
# slack-canvas/bin/verify_scopes.sh
# Verify the Slack bot token has required scopes for Canvas operations
# Usage: verify_scopes.sh

source "$(dirname "$0")/_common.sh"
require_jq

TOKEN=$(resolve_token)

echo "Checking OAuth scopes..."
echo ""

# auth.test validates the token and returns bot/team info.
# Scopes come back in the x-oauth-scopes response header.
HEADER_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE"' EXIT

RESPONSE=$(curl -s -D "$HEADER_FILE" -X POST \
    "https://slack.com/api/auth.test" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}')

if ! echo "$RESPONSE" | jq -e '.ok == true' &>/dev/null; then
    log_error "Token invalid: $(echo "$RESPONSE" | jq -r '.error // "unknown"')"
    exit 1
fi

BOT_NAME=$(echo "$RESPONSE" | jq -r '.user // "unknown"')
TEAM=$(echo "$RESPONSE" | jq -r '.team // "unknown"')
log_info "Authenticated as ${BOT_NAME} in workspace ${TEAM}"

# Extract scopes from response header
GRANTED_SCOPES=$(grep -i '^x-oauth-scopes:' "$HEADER_FILE" | sed 's/^[^:]*: *//' | tr -d '\r')

if [ -z "$GRANTED_SCOPES" ]; then
    log_warn "Could not read scopes from response headers."
    echo "Manually verify at: https://api.slack.com/apps"
    echo ""
    echo "Required scopes: canvases:write, canvases:read"
    exit 0
fi

echo "Granted: ${GRANTED_SCOPES}"
echo ""

REQUIRED=("canvases:write" "canvases:read")
MISSING=()

for req in "${REQUIRED[@]}"; do
    if echo ",$GRANTED_SCOPES," | grep -q ",$req,"; then
        log_info "${req}"
    else
        log_error "${req} — MISSING"
        MISSING+=("$req")
    fi
done

echo ""

if [ ${#MISSING[@]} -gt 0 ]; then
    log_error "Missing scopes: ${MISSING[*]}"
    echo "Add them at: https://api.slack.com/apps → OAuth & Permissions → Scopes"
    echo "Then reinstall the app to your workspace."
    exit 1
fi

log_info "All required scopes present!"
