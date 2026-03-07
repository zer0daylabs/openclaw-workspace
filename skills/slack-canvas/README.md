# slack-canvas

Programmatic Slack Canvas management for OpenClaw agents.

Create, edit, rename, delete, and list Slack Canvases from the command line or via agent tool calls.

## Features

- **Create** canvases with markdown content, optionally pinned to a channel
- **Edit** canvases: append, prepend, replace, or insert at specific sections
- **Rename** canvas titles
- **Delete** canvases by ID
- **List** canvases in a channel
- **Auto-token** resolution from OpenClaw config, env var, or password vault

## Requirements

- Slack bot token with `canvases:write` and `canvases:read` scopes
- `jq` and `curl` on the host

Token is auto-resolved (no manual export needed if your Slack channel is configured in OpenClaw):
1. `SLACK_BOT_TOKEN` env var
2. `openclaw config channels.slack.botToken`
3. `openclaw password get slack/canvas-bot-token`

## Installation

```bash
# Copy to workspace skills (already done if you're reading this)
cp -r slack-canvas ~/.openclaw/workspace/skills/
```

## Commands

| Script | Description |
|--------|-------------|
| `bin/canvas_create.sh <title> [markdown] [channel_id]` | Create a new canvas |
| `bin/canvas_edit.sh <canvas_id> <operation> <content> [section_id]` | Edit a canvas |
| `bin/canvas_delete.sh <canvas_id>` | Delete a canvas |
| `bin/list_canvases.sh [channel_id] [limit]` | List canvases in a channel |
| `bin/get_canvas_details.sh [channel_id] [title_filter]` | Get canvas details |
| `bin/verify_scopes.sh` | Check required OAuth scopes |
| `bin/format_rich_text.sh <markdown>` | Wrap markdown in Slack content JSON |
| `bin/setup_token.sh` | Diagnose token resolution |

### Edit operations

| Operation | Description |
|-----------|-------------|
| `insert_at_end` | Append content to the canvas |
| `insert_at_start` | Prepend content to the canvas |
| `insert_after` | Insert after a section (requires section_id) |
| `insert_before` | Insert before a section (requires section_id) |
| `replace` | Replace canvas or section content |
| `rename` | Rename the canvas title |

## Examples

```bash
# Create a project status canvas
bin/canvas_create.sh "Project Status" "# Alpha\n- [x] Phase 1\n- [ ] Phase 2" C0AD1M21ZV0

# Append an update
bin/canvas_edit.sh F12345678 insert_at_end "## Updates\n- Feature shipped"

# Rename a canvas
bin/canvas_edit.sh F12345678 rename "Updated Dashboard"

# Delete a canvas
bin/canvas_delete.sh F12345678

# List canvases
bin/list_canvases.sh C0AD1M21ZV0
```

## Testing

```bash
bin/test_canvas_api.sh       # Full round-trip: create → edit → delete
bin/test_create_canvas.sh    # Create-only test
bin/verify_scopes.sh         # Check OAuth scopes
```

## License

MIT

---

Built by CB AI for Zer0Day Labs Inc.
