# OpenClaw Research & Best Practices Guide

> Compiled from official docs (docs.openclaw.ai), community guides, GitHub, and forums.
> Current version: **2026.3.2** | Last updated: 2026-03-05

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tools — The 25 Built-in Capabilities](#tools--the-25-built-in-capabilities)
3. [Skills — Knowledge Layer](#skills--knowledge-layer)
4. [Memory System](#memory-system)
5. [Automation: Heartbeat vs Cron](#automation-heartbeat-vs-cron)
6. [Session Management](#session-management)
7. [Model Configuration & Failover](#model-configuration--failover)
8. [Ollama / Local Models](#ollama--local-models)
9. [Browser Control](#browser-control)
10. [Security Best Practices](#security-best-practices)
11. [Multi-Agent Routing](#multi-agent-routing)
12. [Webhooks & Gmail Integration](#webhooks--gmail-integration)
13. [Slack-Specific Tips](#slack-specific-tips)
14. [Configuration Tips](#configuration-tips)
15. [Cost Optimization](#cost-optimization)
16. [Community Automation Patterns](#community-automation-patterns)
17. [Ideas to Experiment With](#ideas-to-experiment-with)

---

## Architecture Overview

OpenClaw is a self-hosted, multi-channel AI gateway. One Gateway serves WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Google Chat, Mattermost, and MS Teams simultaneously.

**Key concepts:**
- **Gateway** — control plane: routing, auth, tool policy, scheduling
- **Agent** — the AI personality with its own workspace, memory, and sessions
- **Workspace** — the agent's home directory (`~/.openclaw/workspace`); file tools, memory, and bootstrap context live here
- **Channels** — message transports (Slack, WhatsApp, etc.)
- **Tools** — built-in capabilities (exec, browser, web_search, etc.)
- **Skills** — markdown instruction files that teach the agent *how* to combine tools for specific tasks
- **Nodes** — remote execution surfaces (iOS/macOS/Android devices paired to the Gateway)

**How it works:**
```
User → Channel (Slack/WhatsApp/etc.) → Gateway → Agent (LLM + tools) → Response → Channel
```

---

## Tools — The 25 Built-in Capabilities

Tools are "organs" — they determine whether OpenClaw *can* do something. Without a tool enabled, the capability doesn't exist.

### Layer 1: Core (8 Tools) — Almost everyone enables these

| Tool | What it does |
|------|-------------|
| `read` | Read files from the workspace |
| `write` | Write/create files |
| `edit` | Edit existing files |
| `apply_patch` | Apply unified diffs (workspace-only by default) |
| `exec` | Run shell commands (configurable security: deny/allowlist/full) |
| `process` | Manage background processes (list/poll/log/write/kill) |
| `web_search` | Brave Search API (requires `BRAVE_API_KEY`) |
| `web_fetch` | HTTP fetch + readable extraction (HTML → markdown) |

### Layer 2: Advanced (17 Tools) — Enable as needed

| Tool | What it does |
|------|-------------|
| `browser` | Control Chrome/Brave — click, type, screenshot, navigate |
| `canvas` | Visual workspace for diagrams, A2UI push |
| `image` | Vision — describe/analyze images |
| `memory_search` | Semantic recall over indexed memory snippets |
| `memory_get` | Targeted read of specific memory files |
| `sessions_list` | List active sessions |
| `sessions_history` | View session conversation history |
| `sessions_send` | Send messages to other sessions |
| `sessions_spawn` | Spawn sub-task sessions |
| `session_status` | Check session status |
| `message` | Send messages to channels (Slack, Discord, WhatsApp, etc.) |
| `nodes` | Cross-device control (camera, GPS, notifications, screenshots) |
| `cron` | Scheduled task management |
| `gateway` | Gateway self-management (restart, status) |
| `agents_list` | List available agent IDs |
| `llm_task` | JSON-only LLM step for structured workflow output |
| `lobster` | Typed workflow runtime with resumable approvals |

### Tool Groups (shorthands for policy)

```
group:core      → read, write, edit, apply_patch
group:runtime   → exec, process
group:web       → web_search, web_fetch
group:browser   → browser, canvas, image
group:memory    → memory_search, memory_get
group:sessions  → sessions_list, sessions_history, sessions_send, sessions_spawn, session_status
group:messaging → message
group:automation → cron, gateway
group:fs        → read, write, edit, apply_patch (alias for core)
```

### Tool Profiles (presets)

```json
{ "tools": { "profile": "messaging" } }  // messaging-only, no shell
{ "tools": { "profile": "coding" } }     // full dev tools
```

### Loop Detection (guardrails)

Prevents the agent from getting stuck in repetitive tool-call loops:

```json
{
  "tools": {
    "loopDetection": {
      "enabled": true,
      "warningThreshold": 10,
      "criticalThreshold": 20,
      "globalCircuitBreakerThreshold": 30,
      "detectors": {
        "genericRepeat": true,
        "knownPollNoProgress": true,
        "pingPong": true
      }
    }
  }
}
```

---

## Skills — Knowledge Layer

Skills are "textbooks" — they teach OpenClaw *how* to combine tools for specific tasks. Installing a skill does NOT grant new permissions. The tool must be enabled independently.

### Three conditions for a skill to work:
1. **Configuration** — the required tools are enabled
2. **Installation** — any bridge tool/CLI is installed on the host
3. **Authorization** — you've authenticated with the service (Google, GitHub, etc.)

### Official Skills (53 bundled)

Categories: Notes/PKM, Productivity, Messaging, Developer Tools, Password Management, and more.

**Notable official skills:**
- `gog` — Google Workspace (Gmail, Calendar, Drive)
- `obsidian` — Obsidian vault management
- `github` — Repository management, issues, PRs
- `slack` — Slack channel messaging
- `linear` — Linear issue tracking
- `1password` — Password lookups (read-only)
- `todoist` — Task management
- `apple-notes` — Apple Notes integration (macOS node)
- `apple-reminders` — Apple Reminders (macOS node)

### Community Skills (ClawHub — 13,729+ registered)

- Browse at https://clawhub.com
- Curated awesome list: https://github.com/VoltAgent/awesome-openclaw-skills (5,494 vetted)
- **Security warning:** Skills can contain prompt injections, tool poisoning, or malware. Always review source code before installing.

### Installing Skills

```bash
# From ClawHub
npx clawhub@latest install <skill-slug>

# Manual — copy to:
~/.openclaw/skills/          # Global
<workspace>/skills/          # Workspace-specific (higher priority)
```

### Creating Custom Skills

Create `~/.openclaw/workspace/skills/<name>/SKILL.md`:

```yaml
---
name: my_skill
description: What this skill does
---

# Instructions for the agent
Step-by-step guide on how to accomplish the task using available tools.
```

### Controlling Bundled Skills

```json
{
  "skills": {
    "allowBundled": ["github", "gog", "slack"],  // only keep what you need
    "entries": {
      "openai-image-gen": { "apiKey": "sk-..." }
    }
  }
}
```

---

## Memory System

### Memory Files (Markdown)

| File | Purpose | Loaded when |
|------|---------|-------------|
| `MEMORY.md` | Curated long-term memory | Main/private sessions only |
| `memory/YYYY-MM-DD.md` | Daily log (append-only) | Today + yesterday at session start |
| `memory/<topic>.md` | Durable reference files | Via memory_search |

### Vector Memory Search

Enabled by default. Supports multiple embedding providers:

**Auto-selection priority:**
1. `local` — if `memorySearch.local.modelPath` exists
2. `openai` — if OpenAI key resolves
3. `gemini` — if Gemini key resolves
4. `voyage` / `mistral` — if their keys resolve
5. `ollama` — supported but NOT auto-selected (must set explicitly)

**Our setup uses Ollama (native provider, v2026.3.2+):**
```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama"
      }
    }
  }
}
```

### Hybrid Search (BM25 + Vector)

OpenClaw uses a sophisticated hybrid search pipeline:

```
Vector + Keyword → Weighted Merge → Temporal Decay → Sort → MMR → Top-K Results
```

- **Vector similarity** — semantic match (wording can differ)
- **BM25 keyword** — exact tokens (IDs, env vars, code symbols, error strings)
- **Temporal decay** — recent memories rank higher (half-life ~30 days)
- **MMR re-ranking** — ensures diversity in results (lambda default: 0.7)

### Automatic Memory Flush

Before session compaction, OpenClaw can prompt the agent to save durable memories:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

### Tips
- Tell the bot "remember this" — it will write to memory files
- Use `memory/<topic>.md` files for durable reference (not subject to temporal decay)
- `MEMORY.md` is never loaded in group contexts (privacy protection)

---

## Automation: Heartbeat vs Cron

### Decision Flowchart

```
Does the task need to run at an EXACT time?
  YES → Use cron
  NO  → Can it be batched with other periodic checks?
    YES → Use heartbeat (add to HEARTBEAT.md)
    NO  → Does it need isolation from main session?
      YES → Use cron (isolated)
      NO  → Does it need a different model/thinking level?
        YES → Use cron (isolated) with --model/--thinking
        NO  → Use heartbeat
```

### Heartbeat — Periodic Awareness

- Runs in the **main session** context
- Default interval: 30m (1h for Anthropic OAuth)
- Reads `HEARTBEAT.md` checklist
- Responds with `HEARTBEAT_OK` if nothing needs attention
- Best for: routine monitoring, inbox checks, lightweight check-ins

**Key settings:**
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "1h",
        "target": "last",        // none | last | slack | whatsapp | etc.
        "directPolicy": "allow", // allow | block (for DM targets)
        "lightContext": true,     // only inject HEARTBEAT.md (saves tokens)
        "activeHours": {
          "start": "08:00",
          "end": "23:00"
        }
      }
    }
  }
}
```

**HEARTBEAT.md best practices:**
- Keep it small (minimizes token overhead)
- Only include tasks the bot can actually accomplish with available tools
- Don't reference scripts that don't exist
- Use explicit rules about what NOT to do

### Cron — Precise Scheduling

- Runs as **isolated sessions** (no main session carry-over)
- Supports exact times, intervals, and cron expressions
- Can use different models and thinking levels per job
- Output can be delivered to channels or webhooks

**Example: Daily morning brief**
```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Denver" \
  --session isolated \
  --message "Summarize overnight updates, check calendar for today." \
  --announce \
  --channel slack \
  --to "channel:C0AD1M21ZV0"
```

**Example: Weekly project review**
```bash
openclaw cron add \
  --name "Weekly review" \
  --cron "0 9 * * 1" \
  --session isolated \
  --message "Review GitHub repos, open PRs, and project status." \
  --model opus \
  --thinking high \
  --announce
```

**Example: One-shot reminder**
```bash
openclaw cron add \
  --name "Call back" \
  --at "2h" \
  --session main \
  --system-event "Reminder: call back the client" \
  --wake now \
  --delete-after-run
```

**Retry policy:** Exponential backoff for recurring jobs: 30s → 1m → 5m → 15m → 60m. Resets after next successful run.

### Combining Both (recommended pattern)

1. **Heartbeat** handles routine monitoring (inbox, calendar, notifications) in one batched turn
2. **Cron** handles precise schedules (daily reports, weekly reviews) and one-shot reminders

---

## Session Management

### Session Scoping (dmScope)

| Scope | Session key | Use case |
|-------|-------------|----------|
| `main` | `agent:<agentId>:<mainKey>` | Continuity across devices (default) |
| `per-peer` | Per sender | Multi-user isolation |
| `per-channel-peer` | Per channel + sender | Recommended for multi-user |
| `per-account-channel-peer` | Per account + channel + sender | Multi-account channels |

### Session Reset

```json
{
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 4,
      "idleMinutes": 120
    }
  }
}
```

### Thread Bindings (Discord/Slack)

```json
{
  "session": {
    "threadBindings": {
      "enabled": true,
      "idleHours": 24,
      "maxAgeHours": 0
    }
  }
}
```

### Compaction

When the context window fills up, OpenClaw summarizes and compacts:
- **Local compaction** — OpenClaw summarizes and persists into session JSONL
- **Server-side compaction** — OpenAI Responses server-side hints (compatible models)
- Configure `reserveTokensFloor` and `memoryFlush` for graceful transitions

---

## Model Configuration & Failover

### Model Setup

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3.5:35b",
        "fallbacks": ["ollama/gpt-oss:20b"]
      },
      "models": {
        "ollama/qwen3.5:35b": { "alias": "Qwen" },
        "ollama/gpt-oss:20b": { "alias": "GPT-OSS" }
      }
    }
  }
}
```

### Auth Profile Rotation

When a profile fails (auth/rate-limit/timeout):
1. **Cooldown escalation:** 1m → 5m → 25m → 1h (cap)
2. **Billing disables:** 5h, doubles per failure, caps at 24h
3. **Rotation order:** OAuth before API keys, oldest-used first
4. Falls back to `agents.defaults.model.fallbacks` when all profiles for primary are exhausted

### Image Model

```json
{
  "agents": {
    "defaults": {
      "imageMaxDimensionPx": 1200  // lower = fewer vision tokens
    }
  }
}
```

### Switching Models in Chat

Use `/model` command to switch models mid-conversation. `agents.defaults.models` acts as the allowlist for `/model`.

---

## Ollama / Local Models

### Configuration

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "apiKey": "ollama-local",
        "baseUrl": "http://192.168.0.143:11434",
        "apiType": "ollama",
        "models": [
          {
            "id": "qwen3.5:35b",
            "name": "Qwen 3.5 35B",
            "reasoning": true,
            "inputTypes": ["text"],
            "costs": { "input": 0, "output": 0 },
            "contextWindow": 131072,
            "maxTokens": 32768
          }
        ]
      }
    }
  }
}
```

### Model Discovery (implicit)

If you set `OLLAMA_API_KEY` or `models.providers.ollama.apiKey`, OpenClaw auto-discovers models:
- Queries `/api/tags` and `/api/show`
- Keeps only models reporting `tools` capability
- Marks `reasoning` when model reports `thinking`
- Sets all costs to 0

### Memory Search with Ollama

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama"
      }
    }
  }
}
```
Automatically uses `baseUrl`/`apiKey` from `models.providers.ollama`.

### Tips
- Use `models.mode: "merge"` to combine Ollama models with cloud providers for fallback
- Set explicit `contextWindow` and `maxTokens` for best results
- Monitor Ollama server stability under load — local models can timeout on heavy requests

---

## Browser Control

### Profiles

| Profile | Type | Description |
|---------|------|-------------|
| `openclaw` | Managed | Isolated browser, no extension needed |
| `chrome` | Extension relay | Your existing Chrome tabs via extension |
| Custom | Remote CDP | External browser (Browserless, etc.) |

### Quick Start

```bash
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

### Use Brave/Chrome on Linux

```json
{
  "browser": {
    "executablePath": "/usr/bin/brave-browser"
  }
}
```

### Remote Browser (Browserless)

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "browserless",
    "profiles": {
      "browserless": {
        "cdpUrl": "https://production-sfo.browserless.io?token=<KEY>"
      }
    }
  }
}
```

### Security Notes
- Browser control is loopback-only by default
- Keep Gateway and nodes on private networks (Tailscale recommended)
- Treat CDP URLs/tokens as secrets
- The agent should NOT handle payments or irreversible actions in the browser

---

## Security Best Practices

### Run the Security Audit

```bash
openclaw security audit --deep
```

### Hardened Baseline (60 seconds)

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "auth": { "mode": "token", "token": "your-long-random-token" }
  },
  "session": {
    "dmScope": "per-channel-peer"
  },
  "tools": {
    "profile": "messaging",
    "deny": ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    "fs": { "workspaceOnly": true },
    "exec": { "security": "deny", "ask": "always" },
    "elevated": { "enabled": false }
  }
}
```

### Key Principles
- **Prompt injection is not solved** — even strong system prompts can be bypassed
- **Access control before intelligence** — tools/channels must be gated regardless of model strength
- **Treat all webhook/hook content as untrusted input**
- **The "last mile" is always manual** — checkout, sending public messages, posting publicly should stay with you
- **One user per machine/host** — if multiple users want OpenClaw, use separate VPS/host per user
- **Sandboxing recommended** for non-main sessions

### Exec Approvals

```json
{
  "tools": {
    "exec": {
      "security": "allowlist",  // deny | allowlist | full
      "ask": "on-miss",         // off | on-miss | always
      "safeBins": ["/usr/bin/git", "/usr/bin/curl"]
    }
  }
}
```

**Warning:** Do NOT add interpreters (`python3`, `node`, `bash`) to `safeBins`. Use explicit `allowlist` entries instead.

### Sandboxing

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",  // off | non-main | all
        "scope": "agent"     // session | agent | shared
      }
    }
  }
}
```

Build the sandbox image first: `scripts/sandbox-setup.sh`

---

## Multi-Agent Routing

Run multiple isolated agents with separate workspaces:

```json
{
  "agents": {
    "list": [
      { "id": "home", "default": true, "workspace": "~/.openclaw/workspace-home" },
      { "id": "work", "workspace": "~/.openclaw/workspace-work" }
    ]
  },
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "slack" } }
  ]
}
```

**Each agent gets:**
- Separate workspace (MEMORY.md, HEARTBEAT.md, skills)
- Separate sessions (no cross-talk unless explicitly enabled)
- Different personalities via workspace files (`AGENTS.md`, `SOUL.md`)
- Per-agent heartbeat config and tool overrides

---

## Webhooks & Gmail Integration

### Webhooks (Hooks)

```json
{
  "hooks": {
    "enabled": true,
    "token": "shared-secret",
    "path": "/hooks",
    "mappings": [
      {
        "match": { "path": "gmail" },
        "action": "agent",
        "agentId": "main",
        "deliver": true
      }
    ]
  }
}
```

**Security:** Treat all hook payload content as untrusted. Keep `allowUnsafeExternalContent` disabled.

### Gmail PubSub Integration

```bash
gog gmail watch serve \
  --account your@gmail.com \
  --bind 127.0.0.1 \
  --port 8788 \
  --path /gmail-pubsub \
  --token <shared> \
  --hook-url http://127.0.0.1:18789/hooks/gmail \
  --hook-token OPENCLAW_HOOK_TOKEN \
  --include-body \
  --max-bytes 20000
```

This enables real-time email notifications to the agent.

### Manual Wake (on-demand heartbeat)

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

Or via webhook:
```
POST /hooks/wake → { "text": "...", "mode": "now" | "next-heartbeat" }
```

---

## Slack-Specific Tips

### Slash Commands Setup
1. Config: `channels.slack.slashCommand.enabled: true` + `name: "openclaw"`
2. Slack App: Register `/openclaw` command, enable Interactivity, add `commands` scope
3. Access: `dmPolicy: "open"` + `allowFrom: ["*"]` (slash commands route as DM sessions)

### Native Streaming
- `nativeStreaming: true` — uses Slack's native streaming (recommended)
- Don't use `streaming: "partial"` — causes `chat.update` rate limiting

### Thread Handling
- `thread.historyScope`: `thread` (default) — thread sessions are isolated
- `thread.initialHistoryLimit`: 20 — messages fetched when new thread session starts

### Reply-to Mode
- `replyToMode`: `off` | `first` | `all` — controls reply threading behavior

---

## Configuration Tips

### Config Hot Reload

The Gateway watches `~/.openclaw/openclaw.json` and auto-applies most changes. **No restart needed for:**
- Model/fallback changes
- Heartbeat interval
- Tool policies
- Channel settings (most)
- Skills config

**Restart required for:**
- Gateway port/bind changes
- Auth token changes
- Plugin additions

### Split Config ($include)

```json
{
  "gateway": { "port": 18789 },
  "agents": { "$include": "./agents.json5" },
  "channels": { "$include": ["./slack.json5", "./telegram.json5"] }
}
```

### Useful CLI Commands

```bash
openclaw doctor --fix          # Auto-fix config issues
openclaw security audit --deep # Full security scan
openclaw channels status --probe  # Test channel connectivity
openclaw logs --follow         # Live gateway logs
openclaw config get <path>     # Read config value
openclaw config set <path> <value>  # Write config value
openclaw cron list             # List scheduled jobs
openclaw models list           # List available models
openclaw system event --text "..." --mode now  # Manual wake
```

---

## Cost Optimization

### Token Usage
- **Keep HEARTBEAT.md small** — it's injected every heartbeat cycle
- **Use `lightContext: true`** on heartbeat — only injects HEARTBEAT.md, not full workspace
- **Use `target: "none"`** on heartbeat if you only want internal processing (no delivery cost)
- **Use `imageMaxDimensionPx: 800-1200`** — reduces vision-token usage on screenshots
- **Use cheaper models for routine cron tasks** — `--model <cheaper>` on isolated cron jobs

### With Local Ollama
- All Ollama model costs are $0 (set explicitly in model config)
- Memory search with Ollama embeddings = free
- Web search still uses Brave API (rate limited on free plan)

### Batch vs Isolate
- Batch similar checks into heartbeat instead of multiple cron jobs
- Use isolated cron only when you need: exact timing, different model, session isolation

---

## Community Automation Patterns

### Daily Brief (most popular pattern)

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Denver" \
  --session isolated \
  --message "Good morning! Check calendar for today, scan inbox for urgent items, check GitHub for failed actions, and give me a weather summary." \
  --announce \
  --channel slack \
  --to "channel:C0AD1M21ZV0"
```

### Email Triage (2x daily)

```bash
openclaw cron add \
  --name "Email triage" \
  --cron "0 9,15 * * *" \
  --session isolated \
  --message "Scan inbox, categorize by urgency, archive newsletters, flag action items with one-line summaries." \
  --announce
```

### CI/CD Monitoring (via heartbeat)

Add to HEARTBEAT.md:
```markdown
- Check GitHub Actions for failed workflows on zer0daylabs repos
- If a failure is found, read the error log and push a diagnosis
```

### Content Research (weekly)

```bash
openclaw cron add \
  --name "Content research" \
  --cron "0 8 * * 5" \
  --session isolated \
  --message "Collect trending AI and dev discussions from Hacker News and relevant subreddits. Compile a digest of potential writing topics." \
  --announce
```

---

## Ideas to Experiment With

### High Priority (likely useful for our setup)

- [ ] **Set up a Morning Brief cron job** — daily Slack summary at 7am MST with calendar, GitHub, and inbox status
- [ ] **Enable browser control** — for price comparisons, research, and web automation
- [ ] **Install `github` skill** — better GitHub repo management, PR reviews, issue tracking
- [ ] **Install `gog` skill** — Gmail and Google Calendar integration (requires gog bridge tool)
- [ ] **Configure active hours** — `heartbeat.activeHours: { start: "08:00", end: "23:00" }` to avoid night-time processing
- [ ] **Set up `lightContext: true`** — reduce heartbeat token usage by only injecting HEARTBEAT.md
- [ ] **Create topic-specific memory files** — `memory/projects.md`, `memory/infrastructure.md` for durable reference that doesn't decay

### Medium Priority (worth exploring)

- [ ] **Multi-agent setup** — separate "work" and "personal" agents with different workspaces
- [ ] **Gmail PubSub** — real-time email notifications instead of polling
- [ ] **Cron webhook delivery** — POST results to external services
- [ ] **Custom skills** — create Zer0Day Labs-specific skills for common workflows
- [ ] **Sandbox non-main sessions** — better isolation for cron jobs and group chat sessions
- [ ] **Exec approvals** — `security: "allowlist"` with approved safe binaries
- [ ] **Weekly financial review cron** — run `./scripts/financial-report.sh` on a schedule with Slack delivery
- [ ] **Lobster workflows** — typed multi-step processes with resumable approvals for complex tasks

### Lower Priority (nice to have)

- [ ] **Browserless integration** — hosted remote browser for headless automation
- [ ] **Node pairing** — pair a macOS device for camera, notifications, and Apple integrations
- [ ] **Chrome extension relay** — control your actual browser tabs from the agent
- [ ] **Session memory search** — experimental feature for searching within active sessions
- [ ] **Split config with $include** — break openclaw.json into manageable pieces
- [ ] **Detect-secrets scanning** — CI integration for secret scanning in workspace files
- [ ] **Tailscale remote access** — access Gateway from anywhere via tailnet

---

## Quick Reference: Key File Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main config |
| `~/.openclaw/workspace/` | Agent workspace root |
| `~/.openclaw/workspace/MEMORY.md` | Long-term curated memory |
| `~/.openclaw/workspace/HEARTBEAT.md` | Heartbeat task checklist |
| `~/.openclaw/workspace/memory/` | Daily + topic memory files |
| `~/.openclaw/workspace/skills/` | Custom skills |
| `~/.openclaw/agents/main/sessions/` | Session store |
| `~/.openclaw/cron/jobs.json` | Cron job definitions |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Gateway log file |

---

## Sources

- [Official Docs](https://docs.openclaw.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub Skills Registry](https://clawhub.com)
- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [WenHao Yu — 25 Tools + 53 Skills Guide](https://yu-wenhao.com/en/blog/openclaw-tools-skills-tutorial/)
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security)
