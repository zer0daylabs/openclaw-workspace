# CB Knowledge Map — Stack Proficiency Tracker

Last updated: 2026-03-24

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
|-----------|------------|-------------|---------------|-------|
| Next.js | working | — | `knowledge/nextjs.md` | MusicGen, AudioStudio, Ringo all use it |
| React | working | — | — | Core of all frontend apps |
| Prisma | basic | — | — | ORM for MusicGen/AudioStudio |
| Stripe | basic | — | `knowledge/stripe.md` | Payments, subscriptions, webhooks |
| Vercel | basic | — | — | Deployment platform for all web apps |
| Tailwind CSS | basic | — | — | Styling framework |
| TypeScript | working | — | — | Primary web language |

## Infrastructure

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Railway | basic | — | — | Database hosting, project management |
| Docker | working | — | — | Freqtrade, Graphiti, Neo4j containers |
| Neo4j | basic | — | — | Graph database for Graphiti |
| Nginx | aware | — | — | May need for reverse proxy setups |
| Linux (Ubuntu) | working | — | — | Host OS |

## Agent System

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| OpenClaw | deep | 2026-03-15 | `OPENCLAW-RESEARCH.md` | Agent runtime, daily use |
| Graphiti | working | 2026-03-15 | — | Temporal knowledge graph |
| Ollama | working | — | — | Local LLM inference server |
| nomic-embed-text | basic | — | — | Embedding model for Graphiti |

## Trading

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Freqtrade | working | 2026-03-09 | `knowledge/freqtrade.md` | Trading bot framework |
| Kraken API | basic | — | — | Exchange API |
| Technical Analysis | basic | — | — | RSI, MACD, Bollinger Bands, etc. |
| Hyperopt/Optuna | basic | 2026-03-18 | `knowledge/hyperopt.md` | Strategy optimization, loss functions |

## Telecom / EventVikings

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| FreeSWITCH | basic | 2026-03-17 | `knowledge/freeswitch.md` | EventVikings predictive dialer depends on it |
| SIP Protocol | aware | 2026-03-21 | `knowledge/sip-protocol.md` | Signaling protocol, core to predictive dialer |
| WebRTC | **working** | **2026-03-23** | `knowledge/webrtc.md` | **RESearched 2026-03-23, moved to working proficiency with foundation, knowledge file created** - Real-time browser-based communication for agent interface |
| Locust | **working** | **2026-03-24** | `knowledge/locust.md` | **RESearched 2026-03-24, moved to working proficiency with foundation, knowledge file created** - EventVikings predictive dialer load testing

## Auth & Identity

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Microsoft 365 / Entra | basic | 2026-03-19 | `knowledge/entra-oauth.md` | OAuth setup, SSO integration |
| OAuth 2.0 | basic | — | — | Used in MS 365, Stripe |
| JWT | basic | — | — | Freqtrade API auth |

## Monitoring & Analytics

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Sentry | basic | 2026-03-18 | `knowledge/sentry.md` | Error tracking, scripts created but not deeply studied |
| PostHog | basic | 2026-03-18 | `knowledge/posthog.md` | A/B testing, feature flags, pricing experiments |

## AI / ML

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| LLM Prompting | working | — | — | Daily use via OpenClaw |
| OpenAI API | basic | — | — | Used by Graphiti for entity extraction |
| Embeddings | basic | — | — | nomic-embed-text for vector search |

---

## Priority Research Queue

Technologies CB should learn next, ordered by mission impact:

1. ✅ **FreeSWITCH** — EventVikings predictive dialer depends on it. RESearched 2026-03-17, moved to basic proficiency.
2. ✅ **Sentry** — Error tracking setup needed. RESearched 2026-03-18, basic proficiency, scripts created.
3. ✅ **PostHog** — A/B testing for pricing. RESearched 2026-03-18, basic proficiency, knowledge file created.
4. ✅ **Hyperopt/Optuna** — Freqtrade strategy optimization. RESearched 2026-03-18, basic proficiency, knowledge file created.
5. ✅ **Microsoft 365 / Entra** — OAuth SSO integration. RESearched 2026-03-19, basic proficiency, knowledge file created.
6. ✅ **Prisma** — Deeper knowledge needed for DB schema changes in MusicGen/AudioStudio. RESearched 2026-03-21, moved to working proficiency, knowledge file created (`memory/knowledge/prisma.md`).
7. ✅ **SIP Protocol** — Critical for EventVikings predictive dialer. RESearched 2026-03-21, moved to aware proficiency with foundation, knowledge file created (`memory/knowledge/sip-protocol.md`).
8. ✅ **WebRTC** — Browser-based real-time communication for agent interface. **RESearched 2026-03-23, moved to working proficiency with foundation, knowledge file created** (`memory/knowledge/webrtc.md`).

9. ✅ **Locust** — Load testing for EventVikings predictive dialer. RESearched 2026-03-24, moved to working proficiency with foundation, knowledge file created (`memory/knowledge/locust.md`)

---

## Update Rules

- Update proficiency level after completing a research task or building something with the tech
- Add `Last Studied` date when you research a topic
- Add `Knowledge File` path when you create a summary
- Add new rows when new technologies enter the stack
- Review this file every 6th heartbeat (~6 hours)
