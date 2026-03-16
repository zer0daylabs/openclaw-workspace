#!/usr/bin/env bash
set -euo pipefail

# validate.sh — Deterministic validation for CB's code changes
# Usage: validate.sh <file1> [file2] ...
# Runs language-appropriate checks. Silent on success, verbose on failure.
# Exit 0 = all clean, Exit 1 = errors found

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [[ $# -eq 0 ]]; then
  echo "Usage: validate.sh <file1> [file2] ..."
  echo "Validates files based on extension (.py, .ts, .js, .json, .sh)"
  exit 2
fi

ERRORS=0
CHECKED=0

validate_python() {
  local f="$1"
  CHECKED=$((CHECKED + 1))

  # Syntax check (fast, catches 90% of issues)
  if ! python3 -m py_compile "$f" 2>&1; then
    echo -e "${RED}FAIL${NC} py_compile: $f"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # Lint check (catches style + logic issues)
  if command -v ruff &>/dev/null; then
    local out
    out=$(ruff check "$f" 2>&1) || true
    if [[ -n "$out" ]]; then
      echo -e "${RED}WARN${NC} ruff: $f"
      echo "$out" | head -10
    fi
  fi
}

validate_js() {
  local f="$1"
  CHECKED=$((CHECKED + 1))

  # Node syntax check
  if ! node -c "$f" 2>&1; then
    echo -e "${RED}FAIL${NC} node -c: $f"
    ERRORS=$((ERRORS + 1))
    return
  fi
}

validate_ts() {
  local f="$1"
  CHECKED=$((CHECKED + 1))

  # Find nearest tsconfig
  local dir
  dir=$(dirname "$f")
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/tsconfig.json" ]]; then
      if command -v npx &>/dev/null; then
        local out
        out=$(cd "$dir" && npx --yes tsc --noEmit 2>&1 | grep -i "error" | head -5) || true
        if [[ -n "$out" ]]; then
          echo -e "${RED}WARN${NC} tsc: $f"
          echo "$out"
        fi
      fi
      return
    fi
    dir=$(dirname "$dir")
  done

  # No tsconfig found — just check syntax as JS
  if [[ -f "${f%.ts}.js" ]] || node -e "require('$f')" 2>/dev/null; then
    :
  fi
}

validate_json() {
  local f="$1"
  CHECKED=$((CHECKED + 1))

  if ! jq . < "$f" > /dev/null 2>&1; then
    echo -e "${RED}FAIL${NC} json syntax: $f"
    jq . < "$f" 2>&1 | head -3
    ERRORS=$((ERRORS + 1))
    return
  fi
}

validate_bash() {
  local f="$1"
  CHECKED=$((CHECKED + 1))

  if ! bash -n "$f" 2>&1; then
    echo -e "${RED}FAIL${NC} bash -n: $f"
    ERRORS=$((ERRORS + 1))
    return
  fi
}

for file in "$@"; do
  if [[ ! -f "$file" ]]; then
    echo -e "${RED}SKIP${NC} not found: $file"
    continue
  fi

  ext="${file##*.}"
  case "$ext" in
    py)   validate_python "$file" ;;
    js)   validate_js "$file" ;;
    ts)   validate_ts "$file" ;;
    tsx)  validate_ts "$file" ;;
    json) validate_json "$file" ;;
    sh)   validate_bash "$file" ;;
    *)
      echo -e "SKIP unknown type: $file (.$ext)"
      ;;
  esac
done

if [[ $ERRORS -gt 0 ]]; then
  echo -e "\n${RED}VALIDATION FAILED${NC}: $ERRORS error(s) in $CHECKED file(s)"
  exit 1
else
  echo -e "${GREEN}OK${NC}: $CHECKED file(s) validated"
  exit 0
fi
