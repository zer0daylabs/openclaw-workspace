# FreeSWITCH Knowledge Base

**Last Updated:** 2026-03-17  
**Proficiency Level:** Basic (from unknown)  
**Research Source:** Web search (GitHub, Medium articles)

---

## Overview

**FreeSWITCH** is an open-source software telephony platform used for:  
- VoIP/SIP communications  
- Predictive dialing systems  
- Contact centers  
- Event-driven call routing

**EventVikings use case:** Predictive dialer for automated call campaigns

---

## Core Concepts

### Architecture
- **Modular design** - Extensible via modules (mod_dialer, mod_event_socket, etc.)
- **Event Socket Interface** - External programs can originate calls via Event Socket
- **Distributed** - Can scale across multiple servers
- **Real-time** - Handles thousands of concurrent calls

### Key Components
1. **Core** - Call routing, media processing
2. **Modules** - SIP, HTTP, WebSocket, database connectors
3. **Event Socket** - API for external control
4. **Directory** - Call routing configuration
5. **Scripts** - Python/Perl integration

### Predictive Dialing
- **Algorithm**: Analyzes call patterns, agent availability
- **Timing**: Predicts optimal time to place next call
- **Benefits**: Reduces agent idle time, increases connection rate

---

## Basic Configuration

### Directory Structure
```
/etc/freeswitch/
├── config/
│   ├── directories/      # User/Voicemail configs
│   ├── dialplan/         # Call routing logic
│   ├── sip_profiles/     # SIP endpoint configs
│   └── xml_ivr_configs/  # IVR configurations
├── scripts/              # Python/Perl scripts
└── sounds/               # Audio files
```

### SIP Configuration (Basic)
```xml
<!-- /etc/freeswitch/sip_profiles/external.xml -->
<profile name="external">
  <variables>
    <variable name="exten-prefix" value=""/>
    <variable name="apply-inbound-acl" value="acl"/>
  </variables>
</profile>
```

### Mod_Dialer Module
GitHub: https://github.com/davidcsi/mod_dialer
- Enables mass call origination
- Connects to IVR or messaging system after connection
- Useful for predictive dialing campaigns

---

## FreeSWITCH CLI Commands

```bash
# Connect to FreeSWITCH CLI
fs_cli

# Essential commands:
show channels           # List active calls
show channels count     # Total active calls
show calls              # Detailed call info
reloadxml              # Reload XML configs
sofia status           # SIP profiles status
sofia profile <name>   # Profile specific info
```

---

## Predictive Dialing Implementation

### High-Level Flow
1. **Dialer Service** queries database for contacts
2. **Algorithm** predicts optimal call timing based on:
   - Historical answer rates
   - Agent availability
   - Time-of-day patterns
3. **Originate Call** via Event Socket or mod_dialer
4. **Monitor Answer** - If answered, transfer to available agent
5. **Rejection Handling** - Busy, no-answer, unanswered numbers

### Event Socket Integration (Python Example)
```python
import freeswitch

# Connect to Event Socket
event_socket = freeswitch.EventSocket("127.0.0.1:8021")
event_socket.connect()

# Originate call
event_socket.execute(
    f" originate {caller} to {dial_string} && answer()"
)
```

---

## Common Use Cases

### Predictive Dialer (EventVikings)
- Automated outbound campaigns
- Agent availability-based call timing
- Skip busy/no-answer numbers
- Track conversion metrics

### VoIP PBX
- Internal extension system
- Call forwarding
- Voicemail integration
- Call recording

### IVR System
- Voice menus
- DTMF input handling
- Database lookups
- Call routing

---

## Best Practices

1. **Security:**
   - ACLs for SIP trunks
   - Rate limiting to prevent abuse
   - Encrypted signaling (TLS)

2. **Performance:**
   - Proper codec selection
   - Media server tuning
   - Connection pooling

3. **Monitoring:**
   - Call detail records (CDR)
   - Real-time call statistics
   - Error logging

4. **Reliability:**
   - High availability setup
   - Call fallbacks
   - Graceful degradation

---

## Related Tools

- **Locust** - Load testing (locustfile.py exists in repo)
- **FreeSWITCH Performance Dialer** - GitHub: voxserv/freeswitch-perf-dialer
- **mod_dialer** - GitHub: davidcsi/mod_dialer

---

## Action Items

1. **Review EventVikings codebase** for FreeSWITCH integration points
2. **Install FreeSWITCH** on dedicated test environment
3. **Study mod_dialer** for predictive dialing implementation
4. **Set up SIP trunks** with telephony provider
5. **Configure dialplan** for EventVikings use case
6. **Integrate with event socket** for call origination

---

## Further Reading

- **Official Docs:** https://freeswitch.org/confluence/display/FREESWITCH/Welcome
- **GitHub mod_dialer:** https://github.com/davidcsi/mod_dialer
- **Predictive Dialing Article:** Medium (see search results)
- **Event Socket API:** FreeSWITCH documentation

---

**Status:** Basic proficiency established. Ready to attempt predictive dialer implementation after additional training/testing.
EOF
cat > ~/.openclaw/workspace/KNOWLEDGE-MAP.md << 'EOF'
# CB Knowledge Map — Stack Proficiency Tracker

Last updated: 2026-03-17

---

## How to Use This File

This file tracks every technology in the Zer0Day Labs stack and CB's proficiency level with each. Use it to:
1. Identify knowledge gaps before attempting tasks
2. Generate research tasks for unfamiliar technologies
3. Track learning progress over time

**Proficiency Levels:**
- **unknown** — Never studied. Cannot attempt tasks involving this tech.
- **aware** — Know what it is, not how to use it. Need research before any task.
- **basic** — Read docs, understand core concepts. Can attempt simple tasks.
- **working** — Have built/modified things with it. Can handle most tasks.
- **deep** — Understand internals, edge cases, best practices. Can debug and optimize.

**Rule:** If proficiency < `basic`, create a research task BEFORE attempting any coding task with that tech. See `LEARNING-PROTOCOL.md`.

---

## Web Applications

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|---|
| Next.js | working | — | `knowledge/nextjs.md` | MusicGen, AudioStudio, Ringo all use it |
| React | working | — | — | Core of all frontend apps |
| Prisma | basic | — | — | ORM for MusicGen/AudioStudio |
| Stripe | basic | — | `knowledge/stripe.md` | Payments, subscriptions, webhooks |
| Vercel | basic | — | — | Deployment platform for all web apps |
| Tailwind CSS | basic | — | — | Styling framework |
| TypeScript | working | — | — | Primary web language |

## Infrastructure

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|---|
| Railway | basic | — | — | Database hosting, project management |
| Docker | working | — | — | Freqtrade, Graphiti, Neo4j containers |
| Neo4j | basic | — | — | Graph database for Graphiti |
| Nginx | aware | — | — | May need for reverse proxy setups |
| Linux (Ubuntu) | working | — | — | Host OS |
| FreeSWITCH | **basic** | **2026-03-17** | **`knowledge/freeswitch.md`** | **VoIP/telephony platform (EventVikings)** |

## Agent System

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|---|
| OpenClaw | deep | 2026-03-15 | `OPENCLAW-RESEARCH.md` | Agent runtime, daily use |
| Graphiti | working | 2026-03-15 | — | Temporal knowledge graph |
| Ollama | working | — | — | Local LLM inference server |
| nomic-embed-text | basic | — | — | Embedding model for Graphiti |

## Trading

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|---|
| Freqtrade | working | 2026-03-09 | `knowledge/freqtrade.md` | Trading bot framework |
| Kraken API | basic | — | — | Exchange API |
| Technical Analysis | basic | — | — | RSI, MACD, Bollinger Bands, etc. |
| Hyperopt/Optuna | aware | — | — | Strategy optimization |

## Telecom / EventVikings

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|
| **FreeSWITCH** | **basic** | **2026-03-17** | **`knowledge/freeswitch.md`** | **VoIP/telephony platform** |
| SIP Protocol | unknown | — | — | Session Initiation Protocol |
| WebRTC | unknown | — | — | Real-time browser communication |
| Locust | aware | — | — | Load testing (locustfile.py exists) |

## Auth & Identity

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|
| Microsoft 365 / Entra | aware | 2026-03-15 | — | OAuth setup started, not completed |
| OAuth 2.0 | basic | — | — | Used in MS 365, Stripe |
| JWT | basic | — | — | Freqtrade API auth |

## Monitoring & Analytics

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|
| Sentry | aware | — | — | Error tracking, scripts created but not deeply studied |
| PostHog | aware | — | — | Product analytics, setup pending |

## AI / ML

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|------|-----|---|---|---|
| LLM Prompting | working | — | — | Daily use via OpenClaw |
| OpenAI API | basic | — | — | Used by Graphiti for entity extraction |
| Embeddings | basic | — | — | nomic-embed-text for vector search |

---

## Priority Research Queue

Technologies CB should learn next, ordered by mission impact:

1. **Hyperopt/Optuna** — Could significantly improve Freqtrade strategy. Currently `aware`.
2. **Prisma** — Deeper knowledge needed for DB schema changes in MusicGen/AudioStudio.
3. **Sentry** — Need to set up proper error tracking. Currently `aware`.
4. **PostHog** — Need for product analytics and A/B testing. Currently `aware`.
5. **Microsoft 365 / Entra** — OAuth integration pending. Currently `aware`.
6. **SIP Protocol** — FreeSWITCH foundation. Currently `unknown`.

---

## Update Rules

- Update proficiency level after completing a research task or building something with the tech
- Add `Last Studied` date when you research a topic
- Add `Knowledge File` path when you create a summary
- Add new rows when new technologies enter the stack
- Review this file every 6th heartbeat (~6 hours)
EOF
