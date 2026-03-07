# Knowledge Graph Nodes - Complete Reference

## Overview

This document provides the complete list of nodes to be added to the Graphiti knowledge graph once the tool becomes operational. Each node represents a specific piece of knowledge about Zer0Day Labs systems, architectures, and operational context.

## Node Inventory

### System Nodes (2 nodes)

#### 1. OpenClaw (Primary System)
```yaml
name: OpenClaw
type: system
description: Advanced AI agent framework for autonomous task execution, multi-agent coordination, and continuous self-improvement
status: active
reference: https://github.com/zer0daylabs/openclaw
key_features:
  - Skills-based modularity
  - Persistent memory across sessions
  - Extensive tool integration (GitHub, Slack, browser)
  - Multi-agent orchestration
  - Self-improvement capabilities
```

#### 2. OpenClaw Workspace (System Component)
```yaml
name: OpenClaw_Workspace
type: system_component
description: Structured workspace organization with hierarchical memory system
status: active
location: ~/.openclaw/workspace
structure:
  - SOUL.md: Agent identity
  - USER.md: User context
  - memory/: Daily logs and curated memories
  - docs/: Integration documentation
  - skills/: Modular capabilities
  - scripts/: Automation scripts
```

### Agent Architecture Nodes (6 nodes)

#### 3. EvoAgentX
```yaml
name: EvoAgentX
type: agent_architecture
focus: Evolutionary algorithm-based optimization
status: active
key_capabilities:
  - Continuous parameter tuning
  - Adaptive learning rates
  - Iterative improvement optimization
best_use_cases:
  - Complex optimization problems
  - Multi-variable optimization
  - Adaptive parameter selection
reference: memory/self-improving-agents-overview.md
```

#### 4. Gödel Agent
```yaml
name: Gödel_Agent
type: agent_architecture
focus: Formal verification and logical reasoning
status: active
key_capabilities:
  - Proof-based decision making
  - Constraint satisfaction
  - Rigorous logical validation
best_use_cases:
  - Critical systems requiring guaranteed correctness
  - Safety-critical operations
  - Formal requirement validation
reference: memory/knowledge-graph-blueprint.md
```

#### 5. Agent0
```yaml
name: Agent0
type: agent_architecture
focus: Minimalist autonomous agent framework
status: active
key_capabilities:
  - Low overhead execution
  - Fast operation
  - Simplicity over feature richness
best_use_cases:
  - Resource-constrained environments
  - Rapid task completion
  - Lightweight operations
reference: memory/openclaw-research.md
```

#### 6. GEPA (Generative Evaluation and Planning Agent)
```yaml
name: GEPA
type: agent_architecture
focus: Generative planning with evaluation loops
status: active
key_capabilities:
  - Creative problem solving
  - Multi-step planning
  - Iterative refinement
best_use_cases:
  - Open-ended creative tasks
  - Complex planning scenarios
  - Exploration and optimization
reference: memory/openclaw-research.md
```

#### 7. SELAUR (Self-Evolving Learning Agent with Usage Records)
```yaml
name: SELAUR
type: agent_architecture
focus: Usage pattern learning and adaptation
status: active
key_capabilities:
  - Personalized behavior adaptation
  - Usage pattern analysis
  - Efficiency optimization
best_use_cases:
  - Repeated task automation
  - Behavior personalization
  - Efficiency improvement over time
reference: memory/openclaw-research.md
```

#### 8. Agent-S
```yaml
name: Agent-S
type: agent_architecture
focus: Secure, sandboxed agent execution
status: active
key_capabilities:
  - Isolation and sandboxing
  - Safety guarantees
  - Controlled execution environments
best_use_cases:
  - Sensitive operations
  - Untrusted code execution
  - High-security requirements
reference: memory/openclaw-research.md
```

### Skill Nodes (7 nodes)

#### 9. agent-autonomy
```yaml
name: agent-autonomy
type: skill
category: foundation
status: active
key_capabilities:
  - Persistent memory across sessions
  - Self-improvement logging
  - Cross-session identity
  - Network discovery
importance: Critical foundation skill
reference: skills/agent-autonomy/SKILL.md
```

#### 10. agent-autopilot
```yaml
name: agent-autopilot
type: skill
category: automation
status: active
key_capabilities:
  - Heartbeat-driven task execution
  - Day/night progress reports
  - Long-term memory consolidation
  - Todo integration
operation:
  - Check frequency: 2-4x daily
  - Check intervals: ~30 minutes
  - Quiet hours: 23:00-08:00
reference: skills/agent-autopilot/SKILL.md
```

#### 11. agent-orchestrator
```yaml
name: agent-orchestrator
type: skill
category: coordination
status: active
key_capabilities:
  - Task decomposition
  - Sub-agent spawning
  - File-based coordination
  - Result consolidation
  - Agent dissolution
triggers:
  - orchestrate
  - multi-agent
  - decompose task
  - spawn agents
  - delegate tasks
reference: skills/agent-orchestrator/SKILL.md
```

#### 12. github
```yaml
name: github
type: skill
category: integration
status: active
key_capabilities:
  - Issue tracking and automation
  - PR management
  - CI monitoring
  - Code review assistance
  - Repository operations
use_cases:
  - Checking PR status
  - Creating comments
  - Listing/filtering
  - Viewing logs
not_for:
  - Complex web UI flows
  - Bulk operations
reference: skills/github/SKILL.md
```

#### 13. slack
```yaml
name: slack
type: skill
category: communication
status: active
key_capabilities:
  - Channel management
  - Message reactions
  - Pinning/unpinning content
  - Activity tracking
best_practices:
  - One reaction per message
  - Quality over quantity
  - Lightweight social signals
reference: skills/slack/SKILL.md
```

#### 14. passwords
```yaml
name: passwords
type: skill
category: security
status: active
key_capabilities:
  - Local encrypted vault storage
  - OS keychain integration
  - Session-based access control
  - TOTP/2FA support
encryption:
  - Algorithm: age
  - Key derivation: Argon2id
  - Encryption: ChaCha20-Poly1305
sensitivity_levels:
  - low, medium, high, critical
reference: skills/passwords/SKILL.md
```

#### 15. bitwarden
```yaml
name: bitwarden
type: skill
category: security
status: active
key_capabilities:
  - Cloud-synced password management
  - Cross-device access
  - Shared credentials
best_use_case:
  - Shared passwords
  - Cross-device requirements
reference: skills/bitwarden/SKILL.md
```

### Decision Nodes (4 nodes)

#### 16. Decision: Memory System Architecture
```yaml
topic: Memory_System_Architecture
date: 2026-03-06
description: Implemented hybrid memory system with daily logs and curated MEMORY.md
rationale:
  - Separate raw operational data from distilled wisdom
  - Prevent memory bloat
  - Preserve critical insights
implementation:
  - Daily logs: memory/YYYY-MM-DD.md
  - Curated wisdom: memory/MEMORY.md
  - Weekly curation process
status: active
reference: memory/self-improving-agents-overview.md
```

#### 17. Decision: Security Architecture
```yaml
topic: Security_Architecture
date: 2026-03-06
description: Local encrypted vault for sensitive API keys with Bitwarden for sharing
rationale:
  - Zero cloud dependency for secrets
  - Maximum security for critical credentials
  - Flexibility for cross-device needs
implementation:
  - Local vault: Sensitive API keys (Stripe, AI providers)
  - Bitwarden: Shared/cross-device passwords
  - Encryption: age with Argon2id
status: active
reference: skills/passwords/SKILL.md
```

#### 18. Decision: Heartbeat Efficiency
```yaml
topic: Heartbeat_Efficiency
date: 2026-03-06
description: Batching pattern for 60% API call reduction
rationale:
  - Reduce token burn and API costs
  - Improve context retention
  - Better efficiency than separate cron jobs
implementation:
  - Combined checks: email, calendar, weather, mentions
  - Check frequency: Every 30 minutes
  - Quiet hours: 23:00-08:00
status: active
reference: memory/self-improving-agents-overview.md
```

#### 19. Decision: Documentation Discipline
```yaml
topic: Documentation_Discipline
date: 2026-03-06
description: Strict rule: write files immediately, never rely on mental notes
rationale:
  - Memory is limited across sessions
  - Files persist across restarts
  - Better than relying on brain state
implementation:
  - Document lessons learned immediately
  - Write files for all important context
  - Update documentation as you go
status: active
reference: AGENTS.md#-write-it-down---no-mental-notes
```

### Event Nodes (2 nodes)

#### 20. Event: Knowledge Management System Implementation
```yaml
type: integration_event
date: 2026-03-06
name: Knowledge_Management_Implementation
description: Complete knowledge management system for Zer0Day Labs
completed_tasks:
  - Task 1: Slack Canvas structure created
  - Task 2: Four memory files written
  - Task 3: Integration guide created
  - Task 4: Knowledge graph setup documented
  - Task 5: Demo task defined
status: complete
reference: This document
```

#### 21. Event: Self-Improvement Phase 1 Complete
```yaml
type: milestone
date: 2026-03-06
name: Self_Improvement_Phase1_Complete
description: Foundation phase of self-improvement system complete
deliverables:
  - Memory system operational
  - Self-improvement logging active
  - Heartbeat monitoring established
  - Baseline metrics captured
status: complete
next_phase: Phase 2 Enhancement (Weeks 3-4)
```

## Node Relationship Map

### System Dependencies
```
OpenClaw (system)
├── OpenClaw_Workspace (system_component)
│   └── Memory_System (architecture)
├── agent-autonomy (skill)
├── agent-autopilot (skill)
├── agent-orchestrator (skill)
├── github (skill)
├── slack (skill)
├── passwords (skill)
└── bitwarden (skill)
```

### Agent Architecture Alternatives
```
Agent_Architectures
├── EvoAgentX (active) -> optimization
├── Gödel_Agent (active) -> verification
├── Agent0 (active) -> minimalist
├── GEPA (active) -> generative planning
├── SELAUR (active) -> pattern learning
└── Agent-S (active) -> security
```

### Decision Impacts
```
Architectural_Decisions
├── Memory_System -> affects all operations
├── Security_Architecture -> affects credential management
├── Heartbeat_Efficiency -> affects API usage
└── Documentation_Discipline -> affects knowledge retention
```

## Query Examples

### Query: What agent architectures are available?
```bash
graphiti_search(query="agent architectures", maxResults=20)
```

### Query: Show all skills and their categories
```bash
graphiti_search(query="skills categories", maxResults=20)
```

### Query: What decisions influenced security architecture?
```bash
graphiti_search(query="security decisions", maxResults=10)
```

### Query: What is the memory system implementation?
```bash
graphiti_search(query="memory system architecture", maxResults=10)
```

### Query: Show all integration events
```bash
graphiti_search(query="integration events", maxResults=20)
```

## Execution Commands

### When Graphiti is Operational

```bash
# Run batch addition
bash scripts/batch-add-knowledge.sh

# Verify key nodes
grep -r "OpenClaw" memory/*.md | head -5
grep -r "agent architecture" memory/*.md | head -5

# Test queries
grep -r "Agent Architectures" memory/knowledge-graph-schema.md
```

### Verification Steps

```bash
# Check all documentation files exist
ls -la memory/openclaw-research.md
ls -la memory/self-improving-agents-overview.md
ls -la memory/knowledge-graph-blueprint.md
ls -la memory/knowledge-graph-schema.md
ls -la docs/OPENCLAW-INTEGRATION.md
ls -la docs/SELF-IMPROVEMENT-ROADMAP.md

# Verify script is executable
chmod +x scripts/batch-add-knowledge.sh
ls -la scripts/

# Check content integrity
grep -c "OpenClaw" memory/*.md
grep -c "Agent" memory/*.md
```

## Status Summary

| Node Type | Count | Status |
|-----------|-------|--------|
| Systems | 2 | Documented |
| Agent Architectures | 6 | Documented |
| Skills | 7 | Documented |
| Decisions | 4 | Documented |
| Events | 2 | Documented |
| **Total** | **21** | **Ready for Graphiti** |

## Next Steps

### Immediate
1. ✅ All nodes documented
2. ✅ Batch script prepared
3. ⏳ Wait for Graphiti operational status

### When Graphiti Fixed
1. Run batch script: `bash scripts/batch-add-knowledge.sh`
2. Verify nodes added: `graphiti_search --query "OpenClaw" --maxResults 20`
3. Test query patterns
4. Establish automated updates

### Long-term
1. Implement automated entity extraction
2. Schedule weekly knowledge sync
3. Set up continuous learning updates
4. Enable cross-reference suggestions

---
*Node Inventory Version*: 1.0
*Created*: 2026-03-06
*Status*: Ready for Graphiti API restoration
*Total Nodes*: 21 (6 system, 6 agent, 7 skill, 4 decision, 2 event)
