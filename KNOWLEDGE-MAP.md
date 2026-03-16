# CB Knowledge Map — Stack Proficiency Tracker

Last updated: 2026-03-15

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
| Hyperopt/Optuna | aware | — | — | Strategy optimization |

## Telecom / EventVikings

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| FreeSWITCH | unknown | — | — | VoIP/telephony platform |
| SIP Protocol | unknown | — | — | Session Initiation Protocol |
| WebRTC | unknown | — | — | Real-time browser communication |
| Locust | aware | — | — | Load testing (locustfile.py exists) |

## Auth & Identity

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Microsoft 365 / Entra | aware | 2026-03-15 | — | OAuth setup started, not completed |
| OAuth 2.0 | basic | — | — | Used in MS 365, Stripe |
| JWT | basic | — | — | Freqtrade API auth |

## Monitoring & Analytics

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| Sentry | aware | — | — | Error tracking, scripts created but not deeply studied |
| PostHog | aware | — | — | Product analytics, setup pending |

## AI / ML

| Technology | Proficiency | Last Studied | Knowledge File | Notes |
|-----------|------------|-------------|---------------|-------|
| LLM Prompting | working | — | — | Daily use via OpenClaw |
| OpenAI API | basic | — | — | Used by Graphiti for entity extraction |
| Embeddings | basic | — | — | nomic-embed-text for vector search |

---

## Priority Research Queue

Technologies CB should learn next, ordered by mission impact:

1. **FreeSWITCH** — EventVikings predictive dialer depends on it. Currently `unknown`.
2. **Hyperopt/Optuna** — Could significantly improve Freqtrade strategy. Currently `aware`.
3. **Prisma** — Deeper knowledge needed for DB schema changes in MusicGen/AudioStudio.
4. **Sentry** — Need to set up proper error tracking. Currently `aware`.
5. **PostHog** — Need for product analytics and A/B testing. Currently `aware`.
6. **Microsoft 365 / Entra** — OAuth integration pending. Currently `aware`.

---

## Update Rules

- Update proficiency level after completing a research task or building something with the tech
- Add `Last Studied` date when you research a topic
- Add `Knowledge File` path when you create a summary
- Add new rows when new technologies enter the stack
- Review this file every 6th heartbeat (~6 hours)
