# DECISIONS.md — Key Calls Made

*Log major decisions to avoid re-litigating later*

## 2026-02-04

### Model Selection
- **Decision:** Switch from Opus to Sonnet for daily work
- **Why:** Cost efficiency for routine tasks
- **Impact:** Lower per-message cost, still high capability

### Organization Structure  
- **Decision:** Use IDEAS.md → PROJECTS.md → DECISIONS.md workflow
- **Why:** Lightweight process for 2-person team
- **Impact:** Clear capture → execution → learning loop

---

## 2026-03-06

### Graphiti Knowledge Graph Status
- **Decision:** Graphiti plugin currently NOT operational - Docker dependency missing
- **Why:** Neo4j + Graphiti API containers require Docker, which is not installed
- **Impact:** Knowledge graph features unavailable, using Obsidian vault structure as alternative storage
- **Action:** Mark for future installation when Docker becomes available

### Ringo Development Priority
- **Decision:** Proceed with Next.js 15 + Supabase stack
- **Why:** Modern, well-supported tech stack, proven reliability
- **Impact:** Foundation for task management platform, ready to execute scaffolding

### Crypto Trading Environment
- **Decision:** Freqtrade with dry-run mode first
- **Why:** Paper trading validates strategy before risking capital
- **Impact:** Environment structure ready, API keys stored securely

### Security Policy
- **Decision:** All API keys stored in password vault, never in config files
- **Why:** Prevent accidental exposure, centralized credential management
- **Impact:** Safer deployment, audit trail for sensitive data

---

## Template
```
### Decision Title
- **Decision:** What we decided
- **Why:** Key reasoning
- **Impact:** Expected effects
```