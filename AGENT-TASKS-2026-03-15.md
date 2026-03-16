# Agent Tasks - Zer0Day Labs Team

**Date:** 2026-03-15  
**Status:** 6 pending tasks assigned  
**Dashboard:** https://app.slack.com/canvas/F0ALLTDTVFF

---

## Assigned Tasks (All Pending)

### **Agent System Tasks (3)**

#### **Task 53** - Microsoft 365 OAuth Setup (High Priority)
- **Category:** Infrastructure
- **ID:** 53
- **Description:** Complete Microsoft 365 OAuth setup for support@zer0daylabs.com
  - Decide on app registration (OAuth) vs password auth
  - Create Microsoft Entra app if needed
  - Configure CLI authentication
  - Test email/calendar operations
- **Documentation:** `MICROSOFT-365-SETUP-2026-03-15.md`

#### **Task 55** - Fix Graphiti Knowledge Graph (Critical)
- **Category:** Agent-System
- **ID:** 55
- **Description:** Fix Graphiti knowledge graph - resolve Neo4j embedding dimension mismatch causing API failures, execute data cleanup/migration, verify knowledge graph operational
- **Impact:** Cannot log agent events/lessons until resolved
- **Last Known Status:** Internal Server Error on API

#### **Task 59** - Test Sub-Agent Orchestration
- **Category:** Agent-System
- **ID:** 59
- **Description:** Test sub-agent orchestration end-to-end
  - Spawn agent-autopilot with agent-orchestrator
  - Verify communication via file-based messaging
  - Test result consolidation
  - Document patterns
- **Tools:** agent-orchestrator, agent-autopilot, task-orchestra

#### **Task 60** - Complete Graphiti Phase 2
- **Category:** Agent-System
- **ID:** 60
- **Description:** Complete Graphiti Phase 2 - implement automatic heartbeat logging to knowledge graph, log significant events (lessons, decisions, milestones), ensure all agent actions are tracked
- **Status:** Waiting for Graphiti to be operational (Task 55)

---

### **Infrastructure Tasks (3)**

#### **Task 56** - Configure Vercel ↔ Railway DATABASE_URL Integration
- **Category:** Infrastructure
- **ID:** 56
- **Description:** Configure Vercel ↔ Railway DATABASE_URL integration
  - Populate railway_db.json with actual DATABASE_URLs from Railway projects
  - Execute auto_vercel_db.py
  - Verify connections in Vercel dashboard
- **Documentation:** `scripts/auto_vercel_db.py`, `docs/railway_db.json`
- **Impact:** Critical for product database connectivity

#### **Task 58** - Setup Monitoring Alerts
- **Category:** Infrastructure
- **ID:** 58
- **Description:** Setup monitoring alerts for MusicGen & AudioStudio
  - Configure Sentry error/latency alerts (15-20 min)
  - Configure PostHog retention/funnel alerts (15-20 min)
  - Slack integration per scripts/setup_alerts_checklist.md
- **Estimated Time:** 35-45 minutes
- **Tools:** Sentry, PostHog, Slack

---

### **Products Task (1)**

#### **Task 57** - Implement Pricing A/B Test
- **Category:** Products
- **ID:** 57
- **Description:** Implement pricing A/B test on MusicGen
  - Execute pricing strategy framework per docs/Pricing-AB-Test-Guide.md
  - Test tiers ($14.99, $19.99, Studio $49.99)
  - Target: +$250-1000 MRR
- **Current MRR:** $9.99
- **Estimated Impact:** High revenue growth potential
- **Documentation:** `docs/Pricing-AB-Test-Guide.md`

---

## Task Status Summary

| Category | Total | Pending | In Progress | Done | Skipped |
|---|------:|--------:|------------:|-----:|--------:|
| Agent-System | 4 | 3 | 0 | 0 | 1 |
| Infrastructure | 6 | 3 | 0 | 0 | 3 |
| Products | 1 | 1 | 0 | 0 | 0 |
| **Total** | **11** | **7** | **0** | **0** | **4** |

---

## Immediate Priorities

### **P0 - Critical (Must Complete)**
1. **Task 55** - Fix Graphiti knowledge graph (blocking all logging)
2. **Task 56** - Vercel ↔ Railway DB integration (blocking product functionality)
3. **Task 53** - Microsoft 365 OAuth setup (blocking email/calendar)

### **P1 - High Priority (Strongly Recommended)**
1. **Task 58** - Setup monitoring alerts (production reliability)
2. **Task 57** - Pricing A/B test (significant revenue opportunity)

### **P2 - Future (Nice to Have)**
1. **Task 59** - Sub-agent orchestration testing (agent evolution)
2. **Task 60** - Graphiti Phase 2 auto-logging (requires 55 to complete)

---

## Dependencies & Blockers

### **Dependencies:**
- Task 60 (Graphiti Phase 2) requires Task 55 (Graphiti fix) to be complete first
- All tasks can run in parallel except 60

### **Blockers:**
- Task 53: Decision needed on OAuth vs password auth
- Task 55: Neo4j data cleanup/migration unknown
- Task 56: DATABASE_URLs need to be collected from Railway projects
- Task 58: Manual UI setup required

---

## Execution Strategy

### **Phase 1: Fix Core Issues (1-2 hours)**
1. Fix Graphiti knowledge graph (Task 55)
2. Implement Microsoft 365 OAuth (Task 53)
3. Configure DB integration (Task 56)

### **Phase 2: Enable Monitoring & Revenue (2-3 hours)**
1. Setup monitoring alerts (Task 58)
2. Implement pricing A/B test (Task 57)

### **Phase 3: Agent Evolution (Ongoing)**
1. Test sub-agent orchestration (Task 59)
2. Complete Graphiti Phase 2 (Task 60)

---

## Links

- **Dashboard:** https://app.slack.com/canvas/F0ALLTDTVFF
- **All Tasks:** See todo list above
- **Documentation:** 
  - `MICROSOFT-365-SETUP-2026-03-15.md`
  - `AGENT-DASHBOARD-2026-03-15.md`
  - `docs/Pricing-AB-Test-Guide.md`
  - `scripts/auto_vercel_db.py`

---

**Created by:** CB - Zer0Day Labs AI Partner  
**Updated:** 2026-03-15 14:00 MST  
**Next Review:** Every heartbeat (~1 hour)
