#!/bin/bash
# Test multiline canvas creation

CONTENT=$'# Project Status

**Last Updated:** 2026-03-06

## MusicGen (edmmusic.studio)
- Active
- MRR: $9.99

## AudioStudio (audiostudio.ai)
- Active

## Infrastructure
- 7 Railway Projects running
- CI/CD: Operational'

bash ~/.openclaw/workspace/skills/slack-canvas/bin/canvas_create.sh "Zer0Day Labs - Project Status" "$CONTENT" "C0AD1M21ZV0"
