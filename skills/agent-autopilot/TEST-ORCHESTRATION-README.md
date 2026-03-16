# Agent Autopilot Orchestration Test

## Test Pattern

**Orchestrator (main agent):** spawns sub-agent → sub-agent executes task autonomously → sub-agent reports back → consolidation

## Execution Flow

1. **Task Assignment:** Main agent creates task for sub-agent
2. **Sub-agent Spawn:** agent-autopilot with agent-orchestrator skill
3. **Autonomous Execution:** Sub-agent reads task, executes work, documents results
4. **Reporting:** Sub-agent updates status.json, writes to outbox/
5. **Consolidation:** Main agent collects results, generates summary

## Key Files Created
- `~/.openclaw/workspace/skills/agent-autopilot/TEST-ORCHESTRATION-README.md`: This file (documentation)
- `~/.openclaw/workspace/memory/orchestration-test-results.md`: Test results and patterns learned
- `status.json`: Sub-agent status tracking

## Expected Outcomes

### Success Patterns
- Sub-agent reads SKILL.md and task instructions
- Performs work autonomously without constant prompting
- Documents findings in structured format
- Completes task within reasonable timebox
- Files properly created in workspace/outbox/

### Failure Patterns (to avoid)
- Sub-agent stalls waiting for prompts
- No documentation of work process
- Task exceeds timebox without completion
- Files not created or incomplete

