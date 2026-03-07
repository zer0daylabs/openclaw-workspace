#!/bin/bash
# slack-canvas/bin/format_rich_text.sh
# Wrap markdown text in Slack's canvas content JSON envelope
# Usage: format_rich_text.sh <markdown_text>
#        echo "## Notes" | format_rich_text.sh -i
#
# Output: {"type":"markdown","markdown":"<escaped content>"}

source "$(dirname "$0")/_common.sh"
require_jq

usage() {
    cat << 'EOF'
Usage: format_rich_text.sh [OPTIONS] <markdown_text>

Wrap markdown in Slack's canvas content JSON object.

Options:
  -h, --help         Show this help
  -i, --interactive  Read from stdin

Output:
  {"type":"markdown","markdown":"..."}

Examples:
  format_rich_text.sh "# Heading\n\n**Bold** text"
  echo "## Notes" | format_rich_text.sh -i
EOF
}

INTERACTIVE=false
MARKDOWN=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        -i|--interactive) INTERACTIVE=true; shift ;;
        *) MARKDOWN="$1"; shift ;;
    esac
done

if [[ "$INTERACTIVE" == true ]]; then
    MARKDOWN=$(cat)
fi

if [ -z "$MARKDOWN" ]; then
    log_error "No markdown text provided"
    usage
    exit 1
fi

# jq handles all JSON escaping correctly
jq -n --arg md "$MARKDOWN" '{type: "markdown", markdown: $md}'
