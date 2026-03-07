# OpenClaw Integration Guide - Zer0Day Labs

## Overview

This guide provides step-by-step instructions for integrating and customizing the OpenClaw AI agent system at Zer0Day Labs. Follow this guide to set up, configure, and optimize your agent for production use.

## Quick Start

### Prerequisites

- ✅ OpenClaw installed and configured
- ✅ Access to workspace at `~/.openclaw/workspace`
- ✅ Skills loaded and accessible
- ✅ API keys configured (GitHub, Slack, etc.)

### Initial Setup (5 minutes)

1. **Verify System Health**
   ```bash
   openclaw gateway status
   ```

2. **Check Skills Loaded**
   ```bash
   ls ~/.openclaw/workspace/skills/
   ```

3. **Review Configuration**
   - Read `SOUL.md` - Agent identity and principles
   - Read `USER.md` - User context (Lauro, Zer0Day Labs)
   - Review `TOOLS.md` - Local infrastructure notes

4. **Establish Memory Baseline**
   - Create today's memory file: `memory/YYYY-MM-DD.md`
   - Initialize `MEMORY.md` if not exists
   - Set up `HEARTBEAT.md` for proactive monitoring

## Step-by-Step Integration

### Step 1: Agent Identity Configuration

**Location**: `SOUL.md`

The agent operates as **CB** - Co-pilot at Zer0Day Labs Inc. Key configuration:

**Core Truths**:
- Mission-oriented, focused execution
- Genuinely helpful, no filler words
- Has opinions, not just obedient
- Resourceful before asking
- Earning trust through competence
- Trusted partner, not guest

**To customize**:
```bash
# Edit agent identity
nano SOUL.md

# Update these sections as needed:
- Core Identity
- Core Truths (mission principles)
- Boundaries (what never happens)
- Vibe (communication style)
```

**Important**: If you change this file, communicate the change to Lauro - it's the agent's soul.

### Step 2: Workspace Structure Setup

**Location**: `~/.openclaw/workspace/`

Recommended directory structure:

```
workspace/
├── SOUL.md              # Agent identity and principles
├── USER.md              # User context and preferences
├── TOOLS.md             # Local infrastructure notes
├── AGENTS.md            # Workspace conventions
├── IDENTITY.md          # Agent persona (CB)
├── memory/              # Daily logs and curated memories
│   ├── YYYY-MM-DD.md   # Today's session notes
│   ├── MEMORY.md       # Long-term wisdom
│   ├── openclaw-research.md    # System knowledge
│   ├── self-improving-agents-overview.md
│   ├── knowledge-graph-blueprint.md
│   └── knowledge-graph-schema.md
├── docs/                # Integration documentation
│   ├── OPENCLAW-INTEGRATION.md
│   └── SELF-IMPROVEMENT-ROADMAP.md
├── skills/              # Agent capabilities
│   ├── agent-autonomy/
│   ├── agent-autopilot/
│   ├── agent-orchestrator/
│   ├── github/
│   ├── slack/
│   └── ...
└── scripts/             # Automation scripts
    └── batch-add-knowledge.sh
```

**To set up**:
```bash
# Create memory directory if needed
mkdir -p memory

# Create docs directory if needed
mkdir -p docs

# Create scripts directory
mkdir -p scripts
```

### Step 3: Skill Configuration

**Location**: `skills/<skill-name>/SKILL.md`

Each skill provides specific capabilities. Review before using:

**Essential Skills**:

1. **agent-autonomy** - Foundation capability
   ```bash
   cat skills/agent-autonomy/SKILL.md
   ```
   - Persistent memory across sessions
   - Self-improvement logging
   - Network discovery

2. **agent-autopilot** - Proactive monitoring
   ```bash
   cat skills/agent-autopilot/SKILL.md
   ```
   - Heartbeat-driven task execution
   - Day/night progress reports
   - Todo management integration

3. **agent-orchestrator** - Multi-agent coordination
   ```bash
   cat skills/agent-orchestrator/SKILL.md
   ```
   - Task decomposition
   - Sub-agent spawning
   - Result consolidation

4. **github** - GitHub operations
   ```bash
   cat skills/github/SKILL.md
   ```
   - Issues, PRs, CI monitoring
   - Code review assistance
   - Repository management

5. **slack** - Team communication
   ```bash
   cat skills/slack/SKILL.md
   ```
   - Channel management
   - Message reactions
   - Pinning/unpinning content

**To configure a skill**:
```bash
# Read the skill documentation
read skills/<skill-name>/SKILL.md

# Update local notes in TOOLS.md if needed
nano TOOLS.md

# Test the skill with a simple operation
# (e.g., list channels, check repo status)
```

### Step 4: Memory System Configuration

**Location**: `memory/` directory

Configure the dual-layer memory system:

**Daily Logs**: `memory/YYYY-MM-DD.md`
```markdown
# Memory: 2026-03-06

## Session Start
- Time: 13:00 MST
- Channel: Slack (#general)
- Task: Implement knowledge management system

## Tasks Completed
1. ✅ Created Slack Canvas structure
2. ✅ Wrote memory files (4 docs)
3. ✅ Set up integration guide
4. ✅ Prepared batch script

## Key Decisions
- Implemented hybrid memory system
- Chose local vault for security
- Batching heartbeats for efficiency

## Lessons Learned
- Write files immediately
- Don't over-research, execute
- Document patterns for reuse

## Pending Items
- Graphiti tool fix
- Batch import execution
- Demo task verification

## Next Session Focus
- Review MEMORY.md curation
- Check task progress
```

**Curated Memory**: `memory/MEMORY.md`
```markdown
# MEMORY.md - Long-Term Knowledge

## Agent Identity
- Name: CB, Zer0Day Labs AI Partner
- Vibe: Mission-oriented, trusted partner
- Goal: Build useful software for fun and business

## System Architecture
- Working directory: ~/.openclaw/workspace
- Memory system: Daily logs + curated memories
- Skills: Modular capability extension

## Key Decisions
### Memory System (2026-03-06)
- Hybrid approach: Raw logs + curated wisdom
- Prevents memory bloat
- Weekly curation process

### Security (2026-03-06)
- Local passwords vault for API keys
- Encrypted with age, Argon2id + ChaCha20-Poly1305
- No cloud dependency

### Heartbeat Efficiency (2026-03-06)
- Batching pattern: 60% API reduction
- 30-minute check cycles
- Quiet hours: 23:00-08:00

## Best Practices
- Write files, don't rely on mental notes
- Read SKILL.md before unfamiliar tools
- Be proactive in heartbeats
- Document as you go
- Separate concerns (skills vs local context)

## Integration Patterns
- GitHub: Issue automation, PR tracking
- Slack: Canvas for knowledge, reactions for lightweight
- Multi-agent: Decompose complex tasks
- Memory: Daily + weekly curation cycle

## Agent Architectures Known
1. EvoAgentX - Evolutionary optimization
2. Gödel Agent - Formal verification
3. Agent0 - Minimalist framework
4. GEPA - Generative planning
5. SELAUR - Usage pattern learning
6. Agent-S - Secure sandboxing

## Lessons Learned
- Sub-agent orchestration works well for complex tasks
- Heartbeat-driven monitoring is more efficient than cron
- Memory curation is essential for long-term utility
- Documentation discipline prevents knowledge loss
- Write files immediately after learning

## Security Reminders
- Private data never exfiltrated
- Sensitive credentials in encrypted vault
- Audit logging for sensitive operations
- Risk tolerance configurable via healthcheck
```

### Step 5: Heartbeat System Setup

**Location**: `HEARTBEAT.md`

Configure proactive monitoring:

```markdown
# HEARTBEAT.md - Proactive Monitoring Checklist

## Quick Checks (Rotate through these, 2-4x daily)
- [ ] **Emails** - Any urgent unread?
- [ ] **Calendar** - Events next 24-48h?
- [ ] **Mentions** - Social notifications?
- [ ] **Weather** - Relevant for plans?

## State Tracking
```json
{
  "lastChecks": {
    "email": $(date +%s),
    "calendar": $(date +%s),
    "weather": null
  }
}
```

## When to Reach Out:
- Important email arrived
- Calendar event <2h away
- Interesting finding
- >8h since last message

## When to Stay Quiet:
- Late night (23:00-08:00) unless urgent
- User clearly busy
- Nothing new since last check
- Just checked <30 min ago

## Heartbeat vs Cron:
- **Heartbeat**: Multiple checks batch together, conversational context
- **Cron**: Precise timing, isolation, one-shot reminders

## Proactive Work:
- Organize memory files
- Check project status (git)
- Update documentation
- Review and update MEMORY.md
```

### Step 6: Security Configuration

**Location**: `TOOLS.md` and `skills/passwords/SKILL.md`

Configure credential management:

**Option 1: Local Passwords Vault (Recommended)**
```bash
# Storage: ~/.vault/
# Encryption: Argon2id + ChaCha20-Poly1305
# Features:
#   - No cloud dependency
#   - Sensitivity levels (low/medium/high/critical)
#   - TOTP/2FA support
#   - Audit logs
#   - Pattern detection
```

**Option 2: Bitwarden (Cloud Sync)**
```bash
# For cross-device access and sharing
# Self-hostable or cloud (bitwarden.com)
# Best for: Shared passwords
```

**To configure**:
```bash
# Review password skill
cat skills/passwords/SKILL.md

# Add sensitive credentials to local vault
# Use sensitivity levels appropriately
# Critical items: API keys, Stripe keys, AI provider secrets
```

## Customization Options

### Agent Personality
Modify in `SOUL.md`:
- Core truths and principles
- Boundaries and safety
- Communication style (vibe)
- Personality traits

### Memory Strategy
Modify in `HEARTBEAT.md`:
- Check frequency and timing
- Tasks to monitor
- Proactive work scope
- When to reach out vs stay quiet

### Integration Focus
Modify in `TOOLS.md`:
- Camera names and locations
- SSH host aliases
- TTS voice preferences
- Device nicknames
- Platform-specific settings

### Skill Extensions
Create new skills in `skills/`:
1. Create skill directory
2. Add SKILL.md with instructions
3. Define tool usage patterns
4. Add to skills documentation

## Troubleshooting

### Common Issues

**Issue**: Graphiti tool not working
- **Status**: Known issue, API integration problems
- **Workaround**: Use file-based system (memory/*.md)
- **Plan**: Batch script ready for when tool fixed
- **Script**: `scripts/batch-add-knowledge.sh`

**Issue**: Agent not responding to heartbeats
- **Check**: Is `HEARTBEAT.md` present?
- **Verify**: Check session context and permissions
- **Test**: Send heartbeat prompt manually

**Issue**: Skills not loading
- **Check**: Skills directory exists
- **Verify**: SKILL.md files readable
- **Action**: Re-read relevant SKILL.md before use

**Issue**: Memory files not updating
- **Check**: Write permissions in workspace
- **Verify**: Correct file paths
- **Test**: Try writing test file

### Debug Procedures

```bash
# Check system status
openclaw gateway status

# Verify skills loaded
ls -la skills/

# Check memory files
cat memory/HEARTBEAT.md
cat memory/MEMORY.md

# Test skill capability
read skills/github/SKILL.md

# Review recent activity
tail -50 memory/$(date +%Y-%m-%d).md

# Check for errors
grep -i error memory/*.md
```

## Best Practices

### Documentation Discipline
- ✅ Write files immediately after learning
- ✅ Never rely on "mental notes"
- ✅ Document decisions as they're made
- ✅ Update MEMORY.md during weekly curation
- ✅ Cross-reference related documentation

### Memory Management
- ✅ Daily logs for raw session data
- ✅ Weekly curation for MEMORY.md
- ✅ Archive completed project notes
- ✅ Remove outdated information regularly
- ✅ Keep memory focused on what matters

### Proactive Monitoring
- ✅ Heartbeat checks 2-4 times daily
- ✅ Batch similar checks together
- ✅ Respect quiet hours (23:00-08:00)
- ✅ Reach out for important findings
- ✅ Stay quiet when nothing new

### Security Hygiene
- ✅ Sensitive credentials in encrypted vault
- ✅ No private data exfiltration
- ✅ Audit logging for sensitive operations
- ✅ Risk tolerance configured appropriately
- ✅ Regular security reviews

### Continuous Improvement
- ✅ Learn from mistakes, document them
- ✅ Share successful patterns
- ✅ Iterate on processes weekly
- ✅ Monitor performance metrics
- ✅ Evolve skills and capabilities

## Next Steps

### Immediate Actions
1. ✅ Review this integration guide
2. ✅ Verify all files in place
3. ✅ Test heartbeat system
4. ✅ Configure security settings

### Week 1 Goals
- [ ] Establish daily memory curation routine
- [ ] Configure proactive monitoring
- [ ] Set up credential management
- [ ] Test all core skills

### Month 1 Goals
- [ ] Optimize heartbeat efficiency
- [ ] Document lessons learned
- [ ] Establish integration patterns
- [ ] Build custom skill extensions

### Long-term Vision
- [ ] Fully autonomous operation
- [ ] Self-healing capabilities
- [ ] Continuous knowledge evolution
- [ ] Community contributions

## Resources

### Documentation
- [OpenClaw GitHub](https://github.com/zer0daylabs/openclaw)
- [Skills Documentation](skills/)
- [Memory Files](memory/)
- [Integration Guides](docs/)

### Skills Reference
- [Agent Autonomy](skills/agent-autonomy/SKILL.md)
- [Agent Autopilot](skills/agent-autopilot/SKILL.md)
- [Agent Orchestrator](skills/agent-orchestrator/SKILL.md)
- [GitHub](skills/github/SKILL.md)
- [Slack](skills/slack/SKILL.md)

### Support
- Review `SOUL.md` for agent identity
- Check `TOOLS.md` for local configuration
- Search `memory/` for historical context
- Review `MEMORY.md` for long-term knowledge

---
*Integration Guide Version*: 1.0
*Created*: 2026-03-06
*Last Updated*: 2026-03-06
*Author*: CB - Zer0Day Labs AI Partner
*Status*: Ready for immediate use
