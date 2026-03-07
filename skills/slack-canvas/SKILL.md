---
name: slack-canvas
description: Create, edit, delete, and list Slack Canvases via the Slack API. Token auto-resolves from OpenClaw config.
homepage: https://github.com/zer0daylabs/slack-canvas
metadata: {"openclaw":{"emoji":"📄","requires":{"scopes":["canvases:write","canvases:read"],"tools":["jq","curl"]}}}
---

# Slack Canvas API Skill

Programmatic Slack Canvas management. Token auto-resolves from `channels.slack.botToken` in openclaw.json — no manual export needed.

## Tools

### canvas_create

Create a new Slack Canvas with markdown content, optionally in a specific channel.

**Usage:**
```bash
bash {baseDir}/bin/canvas_create.sh "TITLE" "MARKDOWN_CONTENT" "CHANNEL_ID"
```

**Parameters:**
- `TITLE` (required): Canvas title
- `MARKDOWN_CONTENT` (optional): Initial markdown content
- `CHANNEL_ID` (optional): Slack channel to pin the canvas to

**Example:**
```bash
bash {baseDir}/bin/canvas_create.sh "Project Status" "# Alpha\n- [x] Phase 1\n- [ ] Phase 2" "C0AD1M21ZV0"
```

### canvas_edit

Edit an existing canvas: append, prepend, replace content, or rename.

**Usage:**
```bash
bash {baseDir}/bin/canvas_edit.sh "CANVAS_ID" "OPERATION" "CONTENT" "SECTION_ID"
```

**Parameters:**
- `CANVAS_ID` (required): The canvas ID (e.g. F12345678)
- `OPERATION` (required): One of `insert_at_end`, `insert_at_start`, `insert_after`, `insert_before`, `replace`, `rename`
- `CONTENT` (required): Markdown content (or new title for rename)
- `SECTION_ID` (optional): Required for insert_after/insert_before

**Examples:**
```bash
bash {baseDir}/bin/canvas_edit.sh "F12345678" "insert_at_end" "## Updates\n- New feature shipped"
```
```bash
bash {baseDir}/bin/canvas_edit.sh "F12345678" "rename" "New Dashboard Title"
```

### canvas_delete

Delete a canvas by ID.

**Usage:**
```bash
bash {baseDir}/bin/canvas_delete.sh "CANVAS_ID"
```

**Example:**
```bash
bash {baseDir}/bin/canvas_delete.sh "F12345678"
```

### list_canvases

List canvases in a Slack channel.

**Usage:**
```bash
bash {baseDir}/bin/list_canvases.sh "CHANNEL_ID" LIMIT
```

**Parameters:**
- `CHANNEL_ID` (optional): Defaults to configured channel
- `LIMIT` (optional): Max results, default 20

**Example:**
```bash
bash {baseDir}/bin/list_canvases.sh "C0AD1M21ZV0" 10
```

### get_canvas_details

Get detailed info about canvases, optionally filtered by title.

**Usage:**
```bash
bash {baseDir}/bin/get_canvas_details.sh "CHANNEL_ID" "TITLE_FILTER"
```

**Example:**
```bash
bash {baseDir}/bin/get_canvas_details.sh "C0AD1M21ZV0" "Project"
```

### verify_scopes

Check that the bot token has the required OAuth scopes.

**Usage:**
```bash
bash {baseDir}/bin/verify_scopes.sh
```

## Important Rules

- **Each command above is a single exec call.** Do not combine multiple commands or add prose to the exec input.
- All scripts auto-resolve the Slack bot token. Do not manually export or hardcode tokens.
- Content uses Slack's markdown format. Use `\n` for newlines within content strings.
- Canvas IDs start with `F` (e.g. `F0AK4PNRCJW`).

## Testing

Smoke test (creates → edits → deletes a test canvas):
```bash
bash {baseDir}/bin/test_canvas_api.sh "CHANNEL_ID"
```

## Prerequisites

- Slack bot token with `canvases:write` and `canvases:read` scopes
- Token auto-resolved from: openclaw.json `channels.slack.botToken`, `SLACK_BOT_TOKEN` env, or password vault
- `jq` and `curl` installed on host
