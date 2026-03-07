# Slack Canvas Integration Guide

This guide walks you through setting up the **Slack Canvas** skill in OpenClaw and demonstrates how to create and edit canvases programmatically.

## 1. Prerequisites

| Item | How to get it | Why it matters |
|------|---------------|----------------|
| Slack App | Create an app in the Slack API portal. | The skill uses the Slack API. |
| OAuth Token | Add **canvases:write** and **canvases:read** scopes. | Needed for creating and editing canvases. |
| OpenClaw | Installed on your machine. | The skill is an OpenClaw agent skill. |
| `jq` | `sudo apt install jq` (or equivalent) | Used by scripts for JSON parsing. |
| `curl` | Comes with most Linux distros | Makes HTTP calls to Slack. |

> **Tip**: Store your bot token securely. For local usage you can set `SLACK_BOT_TOKEN` env var, or use the vault with `openclaw password get slack/canvas-bot-token`.

## 2. Install the Skill

```bash
# Install from the workspace directory
cd /home/lauro/.openclaw/workspace
openclaw skill install ./skills/slack-canvas
```

The `openclaw skill install` command will read `SKILL.md`, copy files into the skills directory, and register the skill.

> If you see an error about missing dependencies, make sure `jq` and `curl` are available.

## 3. Verify OAuth Scopes

```bash
# Run the helper script
slack-canvas/bin/verify_scopes.sh
```

You should see all required scopes granted. If any are missing, follow the instructions in the output.

## 4. Basic Usage

### 4.1 Create a Canvas

```bash
slack-canvas/bin/canvas_create.sh "Project Roadmap" "# Project Roadmap\n\n- Phase 1\n- Phase 2" C0123456789
```

- `Project Roadmap` – optional title.
- Markdown content is converted automatically.
- `C0123456789` – optional channel ID to pin the canvas as a channel tab.

### 4.2 Edit a Canvas

#### Insert at the end

```bash
slack-canvas/bin/canvas_edit.sh insert_at_end F12345678 "## Updated Goals\n- Goal 1\n- Goal 2"
```

#### Replace a section (needs section ID)

1. Find the section ID using `canvases.sections.lookup` or manually in Slack.
2. Replace it:

```bash
slack-canvas/bin/canvas_edit.sh replace F12345678 "- [x] Completed" temp:C:VXX8e648e6984e441c6aa8c61173
```

#### Rename a canvas

```bash
slack-canvas/bin/canvas_edit.sh rename F12345678 '{"type":"markdown","markdown":"New Title :rocket:"}'
```

## 5. Rich Text Conversion

All markdown is automatically wrapped into `expanded_rich_text` objects. If you need to convert raw markdown manually, use:

```bash
slack-canvas/bin/format_rich_text.sh "# Heading\n- Item"
```

The output is a JSON snippet you can embed in a `changes` array.

## 6. Advanced Scenarios

### 6.1 Batch Update

You can script multiple `canvas_edit.sh` calls in a single shell script to perform batch updates.

### 6.2 Integrating with Workflows

If you have a Slack Workflow App, expose these commands as external functions or use the `canvas_edit.sh` script via a webhook.

## 7. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `canvas_creation_failed` | Invalid markdown or unsupported block type | Check formatting; try simpler content |
| `missing_scope` | Bot missing required scopes | Reinstall app with correct scopes |
| `free_teams_cannot_create_standalone_canvases` | Free Slack plan | Use `channel_id` to pin canvas or upgrade plan |
| `canvas_not_found` | Wrong canvas ID or insufficient permissions | Verify ID, ensure token has access |

## 8. Extending the Skill

The skill is open-source. You can add more features such as:

- Listing all canvases in a channel.
- Deleting a canvas.
- Watching for changes via `canvases.update` event.

To contribute, fork the skill directory and open a PR.

---

**Author:** CB – Zer0Day Labs
**License:** MIT
