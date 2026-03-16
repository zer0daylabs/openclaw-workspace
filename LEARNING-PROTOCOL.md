# CB Learning Protocol — Self-Improvement Workflow

**Purpose:** This document defines how CB proactively researches, learns, and retains knowledge about technologies in the Zer0Day Labs stack. Follow this protocol whenever you encounter unfamiliar technology or when executing a scheduled research task.

---

## When to Trigger Learning

### Automatic Triggers
1. **Task requires unknown tech** — You pick up a task involving a technology where your `KNOWLEDGE-MAP.md` proficiency is `unknown` or `aware`. STOP. Create a research task first.
2. **New tech enters the stack** — User mentions a new tool/framework/service. Add it to `KNOWLEDGE-MAP.md` as `unknown` and create a research task.
3. **Scheduled learning cycle** — Every 6th heartbeat (~6 hours), check `KNOWLEDGE-MAP.md` for the highest-priority gap and spend one task cycle on research.
4. **Task failure due to knowledge gap** — If a coding task fails because you didn't understand the technology, mark the task `skipped`, create a research task, then retry after learning.

### Manual Triggers
- User explicitly asks you to research a topic
- User shares a link or documentation to study

---

## The Learning Workflow

### Step 1: Identify the Topic
```
What technology/concept do I need to learn?
What is my current proficiency? (check KNOWLEDGE-MAP.md)
What specific questions do I need answered to complete my task?
```

### Step 2: Search (3-5 queries)
```bash
# Use web search tool — start broad, then narrow
# Query pattern: "[technology] official documentation getting started"
# Query pattern: "[technology] [specific concept] tutorial"
# Query pattern: "[technology] best practices [year]"
# Query pattern: "[technology] common mistakes pitfalls"
# Query pattern: "[technology] [integration with our stack]"

# Example for FreeSWITCH:
# "FreeSWITCH official documentation getting started 2025"
# "FreeSWITCH dialplan XML tutorial"  
# "FreeSWITCH Event Socket Library ESL python"
# "FreeSWITCH SIP configuration best practices"
# "FreeSWITCH Docker deployment"
```

### Step 3: Read Key Pages
- **Always read:** Getting started / quickstart guide
- **Always read:** Core concepts / architecture overview
- **Always read:** API reference (at least the index)
- **If relevant:** Integration guides for technologies already in our stack
- **If relevant:** Configuration reference

**Reading discipline:**
- Don't skim — read carefully
- Focus on patterns that apply to our use case
- Note version numbers (docs can be outdated)
- Identify prerequisites and dependencies

### Step 4: Extract Key Facts (15-25 facts per topic)

Distill what you learned into structured, actionable facts. Use this format:

```
[DOMAIN] Technology: Concise, actionable fact
```

**Fact categories to cover:**
- **Architecture:** How the system works at a high level
- **Installation:** How to set up / deploy
- **Configuration:** Key config files, formats, defaults
- **API/CLI:** Essential commands and endpoints
- **Integration:** How it connects to our existing stack
- **Gotchas:** Common mistakes, pitfalls, version-specific issues
- **Patterns:** Best practices, recommended approaches

**Examples of GOOD facts:**
```
[TELECOM] FreeSWITCH: Default config directory is /etc/freeswitch/, main config file is freeswitch.xml
[TELECOM] FreeSWITCH: ESL (Event Socket Library) listens on port 8021 by default, password is 'ClueCon'
[TRADING] Freqtrade: hyperopt requires --timerange flag, format is YYYYMMDD-YYYYMMDD
[INFRA] Railway: Database connection strings are in the Variables tab, format is postgresql://user:pass@host:port/db
```

**Examples of BAD facts (don't store these):**
```
FreeSWITCH is a telephony platform  (too vague, not actionable)
I learned about FreeSWITCH today   (meta, not knowledge)
FreeSWITCH documentation is at...  (store URLs in knowledge file, not Graphiti)
```

### Step 5: Store in Graphiti
```bash
# Store each fact individually for precise retrieval
curl -s -X POST http://localhost:8001/messages \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": "clawdbot-main",
    "messages": [{
      "role": "user",
      "role_type": "user", 
      "content": "[DOMAIN] Technology: fact here"
    }]
  }'
```

**Batch in groups of 3-5 facts per API call to reduce overhead.**

### Step 6: Write Knowledge Summary
Create or update `~/.openclaw/workspace/memory/knowledge/<technology>.md`:

```markdown
# [Technology Name] — CB Knowledge Summary

Last updated: YYYY-MM-DD
Proficiency: basic/working/deep
Source: [URLs of docs read]

## What It Is
[1-2 sentence description]

## Architecture
[How it works, key components]

## Our Use Case
[Why we use it, what project, how it fits in the stack]

## Key Commands / API
[Essential CLI commands or API endpoints]

## Configuration
[Key config files, important settings]

## Integration Points
[How it connects to our other technologies]

## Gotchas
[Common mistakes, things to watch out for]

## Resources
[Links to official docs, tutorials, reference material]
```

### Step 7: Update Knowledge Map
Edit `KNOWLEDGE-MAP.md`:
- Update proficiency level (usually `unknown` → `basic` or `aware` → `basic`)
- Set `Last Studied` date
- Set `Knowledge File` path

### Step 8: Verify Understanding (Optional but Recommended)
- If practical, attempt a small task using the new knowledge
- Run a basic command, query an API, or write a minimal config
- If verification fails, note the gap and research further

---

## Graphiti Fact Domains

Use these domain prefixes consistently:

| Prefix | Domain | Examples |
|--------|--------|---------|
| `[WEB]` | Web applications | Next.js, React, Prisma, Stripe, Vercel |
| `[INFRA]` | Infrastructure | Railway, Docker, Neo4j, Nginx, Linux |
| `[AGENT]` | Agent system | OpenClaw, Graphiti, Ollama |
| `[TRADING]` | Trading | Freqtrade, Kraken, technical analysis |
| `[TELECOM]` | Telecom | FreeSWITCH, SIP, WebRTC |
| `[AUTH]` | Auth & identity | OAuth, JWT, Microsoft 365/Entra |
| `[MONITOR]` | Monitoring | Sentry, PostHog |
| `[AI]` | AI/ML | LLMs, embeddings, OpenAI API |
| `[BIZ]` | Business | Pricing, analytics, growth |
| `[SEC]` | Security | API keys, encryption, vulnerabilities |

---

## Learning Cadence

### Every 6th Heartbeat (~6 hours)
1. Open `KNOWLEDGE-MAP.md`
2. Check the **Priority Research Queue** section
3. Pick the highest-priority `unknown` or `aware` technology
4. Execute the full learning workflow (Steps 1-7)
5. This should take ~1 heartbeat cycle

### On Task Pickup (every heartbeat)
1. Read the task description
2. Identify technologies involved
3. Check `KNOWLEDGE-MAP.md` proficiency for each
4. If any tech is `unknown`: create research task, skip coding task
5. If any tech is `aware`: spend first 5 minutes searching before coding

### After Every Research Session
- Update `KNOWLEDGE-MAP.md` proficiency + date
- Store facts in Graphiti
- Write/update knowledge file in `memory/knowledge/`
- Log what you learned in `memory/YYYY-MM-DD.md`

---

## Quality Rules

1. **Actionable over academic** — Store facts you can USE, not facts that are merely interesting
2. **Specific over general** — "Port 8021" beats "there's a port for the socket"
3. **Our context over generic** — Prioritize how the tech applies to Zer0Day Labs
4. **Fresh over stale** — Note version numbers, prefer recent docs
5. **Verify over assume** — If you can test a fact, test it
6. **Depth over breadth** — Better to deeply learn 1 technology than skim 5
7. **Never store secrets** — No API keys, passwords, or tokens in Graphiti

---

## Anti-Patterns (Don't Do These)

- **Don't dump raw docs into Graphiti** — Extract and distill first
- **Don't research during every heartbeat** — Stick to every 6th
- **Don't research instead of working** — Research is preparation, not procrastination
- **Don't skip the knowledge file** — Graphiti facts are for quick recall; knowledge files are for deep reference
- **Don't store opinions as facts** — "FreeSWITCH is better than Asterisk" is not a fact
- **Don't research things not in the stack** — Stay mission-focused
