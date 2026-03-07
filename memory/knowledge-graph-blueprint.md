# Knowledge Graph Blueprint - Self-Aware Agent System Schema

## Executive Overview

This document defines the schema and architecture for a self-aware agent knowledge graph using Graphiti API. The system enables persistent fact storage, relationship mapping, and temporal reasoning about agent behavior, decisions, and learning.

## System Architecture

### Core Components

1. **Graphiti API**: Temporal knowledge graph backend
2. **Node Types**: Entity classification (OpenClaw, Agent types, Skills, Decisions)
3. **Edge Types**: Relationship definitions (uses, implements, learned, deprecated)
4. **Temporal Dimension**: Timestamped fact storage and querying
5. **Entity Extractor**: Automatic identification of concepts and relationships

## Schema Definition

### Node Categories

#### 1. System Nodes
**Purpose**: Represent core systems and platforms

**Attributes**:
- `name`: System identifier
- `type`: "system" or "platform"
- `description`: Functional overview
- `version`: Current version (if applicable)
- `status`: "active", "deprecated", "planned"
- `created`: Timestamp of first appearance

**Example**:
```
{ "name": "OpenClaw", "type": "system", "description": "AI agent framework", "status": "active", "created": "2026-03-06" }
```

#### 2. Agent Nodes
**Purpose**: Document agent architectures and implementations

**Attributes**:
- `name`: Agent name (EvoAgentX, Gödel Agent, etc.)
- `type`: "agent_architecture"
- `focus`: Primary specialization
- `strengths`: List of key capabilities
- `use_cases`: Recommended application scenarios
- `status`: "active", "experimental", "deprecated"
- `reference`: Link to documentation or repository

**Example**:
```
{ "name": "EvoAgentX", "type": "agent_architecture", "focus": "Evolutionary optimization", "strengths": ["parameter tuning", "adaptive learning"], "use_cases": ["complex optimization"], "status": "active" }
```

#### 3. Skill Nodes
**Purpose**: Document available capabilities and tools

**Attributes**:
- `name`: Skill identifier
- `type": "skill"
- `category`: "execution", "integration", "analysis", "automation"
- `purpose`: What it accomplishes
- `dependencies`: Required skills or systems
- `usage_pattern`: Typical invocation context
- `skill_path`: File location of SKILL.md

**Example**:
```
{ "name": "agent-orchestrator", "type": "skill", "category": "automation", "purpose": "Multi-agent task decomposition", "skill_path": "~/workspace/skills/agent-orchestrator/SKILL.md" }
```

#### 4. Decision Nodes
**Purpose**: Record architectural and implementation decisions

**Attributes**:
- `topic`: Decision subject
- `description`: What was decided
- `date`: Decision timestamp
- `rationale`: Reasoning behind decision
- `context`: Circumstances at decision time
- `alternative_considered`: Other options evaluated
- `status": "active", "reconsidered", "reversed"

**Example**:
```
{ "topic": "Memory System", "description": "Implement daily logs + curated MEMORY.md", "rationale": "Separate raw data from insights", "date": "2026-03-06" }
```

#### 5. Event Nodes
**Purpose**: Track significant occurrences and milestones

**Attributes**:
- `name`: Event identifier
- `type": "event_type" (integration, milestone, issue, deployment)
- `date`: When it occurred
- `description`: What happened
- `outcome`: Result or status
- `related_entities`: Linked nodes

**Example**:
```
{ "name": "Knowledge Graph Integration", "type": "integration", "date": "2026-03-06", "description": "Implement Graphati-based knowledge storage", "outcome": "In progress" }
```

### Edge Types

#### Relationship Definitions

1. **USES**
   - Agent uses Skill
   - System uses Tool
   - Example: EvoAgentX uses agent-autonomy

2. **IMPLEMENTATION_OF**
   - Agent implements Architecture pattern
   - Example: Agent0 implements minimalist pattern

3. **DEPENDS_ON**
   - Skill requires another skill
   - System depends on platform
   - Example: agent-orchestrator depends on memory persistence

4. **LEARNED**
   - Decision results from learning
   - System evolves from previous version
   - Example: Memory curation learned from verbosity issues

5. **SOLUTION_FOR**
   - Decision solves specific problem
   - Implementation addresses known gap
   - Example: Heartbeat pattern solves API call efficiency

6. **DEPRECATED_BY**
   - Older pattern replaced by new approach
   - Example: Multiple cron jobs deprecated by heartbeat batching

## Integration Patterns

### Agent Self-Documentation

```python
# When agent makes significant decision:
graphiti_store(
    fact="Decision: Implement daily memory curation process",
    speaker="CB-Agent",
    context="Memory management optimization",
    timestamp="2026-03-06T13:00:00Z"
)

# When agent learns from experience:
graphiti_store(
    fact="Lesson: Write files immediately instead of relying on mental notes",
    speaker="CB-Agent",
    context="Post-mortem analysis of session 3847",
    timestamp="2026-03-06T14:30:00Z"
)
```

### Knowledge Graph Query Patterns

**Query: What agent architectures are currently active?**
```graphiti_search(query="active agent architectures", maxResults=20)
```

**Query: What decisions has the agent made about memory management?**
```graphiti_search(query="memory management decisions", maxResults=20)
```

**Query: What skills does agent-orchestrator depend on?**
```graphiti_search(query="agent-orchestrator dependencies", maxResults=20)
```

### Entity Extraction Automation

When processing new information, automatically extract:
- **People**: Lauro, CB, team members
- **Systems**: OpenClaw, Slack, GitHub, Graphiti
- **Decisions**: Architectural choices, integration patterns
- **Events**: Milestones, deployments, issues
- **Skills**: Tool capabilities and usages

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Fix Graphiti API integration issues
- [ ] Establish node naming conventions
- [ ] Create initial system nodes (OpenClaw, core skills)
- [ ] Document existing agent architectures
- [ ] Test basic add/search operations

### Phase 2: Expansion (Weeks 2-3)
- [ ] Add decision nodes for all major architectural choices
- [ ] Map skill dependencies and relationships
- [ ] Document integration events and milestones
- [ ] Implement entity extraction from session logs
- [ ] Create batch import script for historical data

### Phase 3: Autonomy (Weeks 4+)
- [ ] Automated node creation from agent actions
- [ ] Self-documentation of learning episodes
- [ ] Query-driven self-analysis and reporting
- [ ] Cross-reference suggestions during operations
- [ ] Performance optimization recommendations

## Batch Import Script Template

```bash
#!/bin/bash
# batch-add-knowledge.sh
# Purpose: Add multiple knowledge nodes when Graphiti is operational

NODES_TO_ADD=(
  "OpenClaw:system:AI agent framework for autonomous task execution:active:https://github.com/zer0daylabs/openclaw"
  "EvoAgentX:agent_architecture:Evolutionary optimization with adaptive learning:active:~/workspace/memory/self-improving-agents-overview.md"
  "Godel Agent:agent_architecture:Formal verification and logical reasoning:active:~/workspace/memory/knowledge-graph-blueprint.md"
  "Agent0:agent_architecture:Minimalist autonomous agent framework:active:~/workspace/memory/openclaw-research.md"
  "GEPA:agent_architecture:Generative planning with evaluation loops:active:~/workspace/memory/openclaw-research.md"
  "SELAUR:agent_architecture:Usage pattern learning and adaptation:active:~/workspace/memory/openclaw-research.md"
  "Agent-S:agent_architecture:Secure sandboxed execution:active:~/workspace/memory/openclaw-research.md"
  "agent-autonomy:skill:Persistent memory and self-improvement logging:active:~/workspace/skills/agent-autonomy/SKILL.md"
  "agent-autopilot:skill:Heartbeat-driven task management:active:~/workspace/skills/agent-autopilot/SKILL.md"
  "agent-orchestrator:skill:Multi-agent decomposition and coordination:active:~/workspace/skills/agent-orchestrator/SKILL.md"
)

for node in "${NODES_TO_ADD[@]}"; do
  IFS=':' read -r name type description status ref <<< "$node"
  echo "Adding node: $name ($type)"
  # graphiti_store command will be added once API is fixed
  # graphiti_store --node "$name" --type "$type" --description "$description" --status "$status" --reference "$ref"
done

echo "Batch import complete. Review results."
```

## Query and Analysis Patterns

### Self-Assessment Queries

1. **Capability Mapping**:
   "What skills does the agent currently have and how are they used?"

2. **Learning Audit**:
   "What lessons have been learned in the past week?"

3. **Decision Traceability**:
   "Show all decisions related to memory management and their evolution"

4. **Integration Status**:
   "What systems are integrated and what are their dependencies?"

### Operational Queries

- **Before executing complex task**: Query related past experiences
- **After failure**: Query similar failure patterns and solutions
- **When optimizing**: Query performance patterns and bottlenecks
- **During integration**: Query related integrations and lessons learned

## Security and Privacy

### Data Classification
- **Public**: System descriptions, skill lists, architecture overviews
- **Internal**: Decision rationale, integration details, performance metrics
- **Private**: Personal preferences, sensitive context, security configurations

### Query Security
- Never query or store sensitive credentials
- Filter personal context from shared sessions
- Audit log all knowledge additions and queries
- Implement access control based on session context

## Maintenance and Evolution

### Regular Tasks
1. **Weekly**: Review and deduplicate nodes
2. **Monthly**: Archive deprecated systems and patterns
3. **Quarterly**: Update version information and status
4. **Annually**: Full schema review and optimization

### Schema Evolution
- Version all schema changes
- Maintain backward compatibility for existing queries
- Document migration paths when removing or modifying node types
- Track breaking changes and their impact

---
*Blueprint Version*: 1.0
*Created*: 2026-03-06
*Author*: CB - Zer0Day Labs AI Partner
*Status*: Ready for implementation pending Graphiti API resolution
