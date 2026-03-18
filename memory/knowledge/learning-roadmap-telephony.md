# Telephony & Infrastructure Learning Roadmap

**Date:** 2026-03-17  
**Status:** In Progress  
**Goal:** Master Kamailio, React, FreeSWITCH, HAProxy, Fail2Ban, OpenSIPS

---

## Technology Overview

### 1. Kamailio ✅ COMPLETED
**Type:** SIP Proxy Server (Signaling)
**Current Status:** Phase 1 Complete
**Proficiency:** `aware` → learning

**What it is:**
- High-performance Open Source SIP Server (successor of OpenSER/SER)
- Handles **thousands of call setups per second**
- Carrier-grade VoIP platform foundation
- Written in C for Unix/Linux with architecture-specific optimizations
- **License:** GPLv2+ (started 2001, merged 2008)

**Core Capabilities:**
- SIP proxy (stateful/stateless), load balancer
- Least cost routing, SIP firewall, edge proxy, SBC
- Registrar, location service, presence, instant messaging
- MSRP, WebRTC, IPv4/IPv6, IMS/VoLTE, ENUM
- **Backend support:** MySQL, PostgreSQL, Oracle, RADIUS, LDAP, Redis, Cassandra, MongoDB, Memcached

**EventVikings Use Case:**
```
SIP Trunk → Kamailio (routing/auth) → FreeSWITCH (media/IVR)
```

**Status:** Knowledge base created, Graphiti facts queued (processing)

---

### 2. OpenSIPS 🔄 NEXT PRIORITY
**Type:** SIP Proxy Server (Signaling)
**Current Status:** Not Started
**Proficiency:** `unknown`

**What it is:**
- **Multi-functional SIP server** used by carriers, telecoms, ITSPs
- **Tens of thousands CPS**, millions of simultaneous calls
- **120+ modules** for SIP handling, backend operations, integration
- **Stable releases:** 3.6.4, 3.4.17 (LTS)
- **Recent:** Bond sockets in 4.0 (March 2026)

**Key Features:**
- Class4/5 Residential Platforms
- Trunking/Wholesale
- Enterprise/Virtual PBX Solutions
- Session Border Controllers
- Application Servers
- Front-end Load Balancers
- IMS Platforms
- Call Centers

**Recent Developments (2026):**
- Bond sockets for DNS-based destination selection
- Proxy Protocol support for HAProxy integration
- Dynamic branch allocation (no memory penalties)
- Runtime configuration using Config module
- Unified SIP branches correlation
- Structured SDP manipulation
- Sockets Management at runtime

**Documentation:**
- Manual: https://www.opensips.org/Documentation/Manuals
- Modules: https://www.opensips.org/Documentation/Modules-3-4
- Community: https://www.opensips.org/Community/OpenSIPS-CE

**Kamailio vs OpenSIPS:**
- Both are carrier-grade SIP proxies
- **Similarity:** Config-driven routing, 100+ modules, SQL backends
- **Difference:** Kamailio more modular/flexible, OpenSIPS stronger in carrier deployments

---

### 3. FreeSWITCH 🔄 FOLLOW-UP
**Type:** Media Server (Signaling + Media)
**Current Status:** Not Started
**Proficiency:** `unknown`

**What it is:**
- **Leading open-source communication framework**
- Powers 5K+ businesses, 300M+ daily users
- Maintained by SignalWire (founded by core developers)
- Direct access to media and signaling layers
- Modular architecture, flexible APIs

**Core Capabilities:**
- **Voice, video, text communications** from IP Network and PSTN
- WebRTC, VoIP, video transcoding
- MCU (Multipoint Control Unit) for conferencing
- SIP features, dialplans, routing logic
- **Codecs:** Speex, G.722, G.722.1 (Siren), SILK, BroadVoice, HD audio
- Direct media bypass and proxy

**Commercial Modules:**
- **G.729A:** $10/call - efficient 8kbit/s speech coder
- **AMD (Answering Machine Detection):** $50 - human vs machine detection for autodialers
- **FreeSWITCH Advantage:** Supported distribution, quarterly releases

**EventVikings Integration:**
- Kamailio routes → FreeSWITCH handles media/IVR/recording
- Predictive dialer call flows
- Multi-party conferencing
- Voice automation and AI integration

**Documentation:**
- Main docs: https://signalwire.com/freeswitch
- Developer docs: https://developer.signalwire.com/freeswitch
- Conference: ClueCon Aug 10-14, 2026

**SignalWire Relationship:**
- FreeSWITCH gives control, SignalWire handles scaling
- Cloud platform for enterprise deployments
- Zero re-architecting needed when growing

---

### 4. HAProxy 🔄 BACKEND INFRASTRUCTURE
**Type:** Load Balancer / Reverse Proxy (TCP/HTTP)
**Current Status:** Not Started
**Proficiency:** `unknown`

**What it is:**
- **De-facto standard open-source load balancer**
- High availability, load balancing, proxying for TCP/HTTP apps
- **Performance:** 2M+ HTTP requests/sec over SSL, 100 Gbps forwarded traffic
- **Started 2002**, one of oldest continuously maintained projects
- **License:** GPLv2+

**Core Features:**
- **Event-driven architecture** (reacts to I/O events instantly)
- SMP parallelism via multi-threading
- Thread-aware load balancing (3.2+)
- Built-in stats interface
- Active health checks
- SSL/TLS termination
- HTTP/2, HTTP/3 (QUIC) support
- Lua scripting for custom logic

**Current Versions (2026):**
- **3.4-dev6** (2026-03-05) - Dev branch
- **3.3.5** (2026-03-09) - Stable (EOL 2027-Q1)
- **3.2.14** (2026-03-09) - LTS (EOL 2030-Q2)
- **3.0.18** (2026-03-09) - LTS (EOL 2029-Q2)
- **2.8.19** (2026-03-09) - LTS (EOL 2028-Q2)

**Recent Highlights:**
- 3.3: QUIC backend, persistent stats, KTLS, TLS ECH
- 3.2: ACME/SSL, CPU scalability improvements
- Security: CVE-2026-26080/26081 fixed (QUIC parsing)

**Documentation:**
- Manual: http://docs.haproxy.org/
- Intro: http://docs.haproxy.org/dev/intro.html
- GitHub: https://github.com/haproxy/haproxy
- Demo: http://demo.haproxy.org/

**EventVikings Use Case:**
- Load balance Kamailio/OpenSIPS instances
- HTTP API load balancing
- SSL termination for web apps
- Health monitoring and failover
- Stats dashboard (built-in)

---

### 5. Fail2Ban 🔄 SECURITY LAYER
**Type:** Intrusion Prevention System (IPS)
**Current Status:** Not Started
**Proficiency:** `unknown`

**What it is:**
- Python-based intrusion prevention framework
- Monitors log files, bans IPs showing malicious behavior
- **Prevents brute force attacks**, DoS attempts
- Flexible filtering, jail system

**Core Features:**
- **Log monitoring** via regular expressions
- **Ban mechanisms:** iptables, firewalld, IPset, custom actions
- **Jail system:** Pre-defined filters for SSH, Apache, Nginx, mail servers
- **Recidive jail:** Ban repeat offenders longer
- **Integration:** Can work with HAProxy, web servers, SSH

**EventVikings Use Case:**
- Protect Kamailio/OpenSIPS from SIP flood attacks
- Block brute force on web admin panels
- SSH hardening
- Rate limiting for API endpoints
- Complement HAProxy rate limiting

**Documentation:**
- Main: https://fail2ban.readthedocs.io/
- GitHub: https://github.com/fail2ban/fail2ban
- Configuration examples: `/etc/fail2ban/jail.conf`

**Integration Patterns:**
```
SSH Service → fail2ban-sshd
Nginx/Apache → fail2ban-httpd
Kamailio logs → custom filter
HAProxy logs → fail2ban-haproxy
```

---

### 6. React 🔄 FRONTEND FRAMEWORK
**Type:** JavaScript UI Library
**Current Status:** Not Started
**Proficiency:** `unknown`

**What it is:**
- **Declarative, component-based** JavaScript library for UI
- **Created by Facebook/Meta** (2013)
- **Virtual DOM** for efficient rendering
- **One-way data flow** for predictable state management
- **Ecosystem:** Next.js, Redux, React Native

**Core Concepts:**
- **Components:** Functional (hooks) or Class-based
- **JSX:** HTML-like syntax in JavaScript
- **State:** Local component state via `useState`
- **Effects:** Side effects via `useEffect`
- **Props:** Parent-to-child data passing
- **Hooks:** `useState`, `useEffect`, `useContext`, custom hooks

**Documentation:**
- Main: https://react.dev (new docs, 2023+)
- Tutorial: https://react.dev/learn
- GitHub: https://github.com/facebook/react
- Ecosystem: https://nextjs.org, https://redux.js.org

**EventVikings Use Case:**
- Dashboard UI for predictive dialer
- Real-time call metrics visualization
- Agent management interface
- Integration with HAProxy/Fail2Ban monitoring
- WebRTC call controls

---

## Learning Plan Summary

### Current State:
- ✅ **Kamailio:** Research complete (6.9KB knowledge base, Graphiti facts queued)
- 🔄 **OpenSIPS:** Next target (SIP proxy sibling to Kamailio)
- 🔄 **FreeSWITCH:** Critical for EventVikings (media server integration)
- 🔄 **HAProxy:** Infrastructure backbone (load balancing)
- 🔄 **Fail2Ban:** Security hardening (intrusion prevention)
- 🔄 **React:** Frontend framework (UI/dashboard)

### Recommended Learning Order:

**Phase 1: Signaling Layer** (SIP Proxy)
1. ✅ Kamailio (done) → Deep dive into EventVikings config
2. OpenSIPS → Compare/contrast with Kamailio, migration paths

**Phase 2: Media Layer** (FreeSWITCH)
3. FreeSWITCH → Integration with Kamailio/OpenSIPS, call flows

**Phase 3: Infrastructure** (Load Balancing + Security)
4. HAProxy → Load balance Kamailio/OpenSIPS/FreeSWITCH, SSL termination
5. Fail2Ban → Protect all services, brute force prevention

**Phase 4: Frontend** (User Interface)
6. React → Dashboard, metrics, management interface

### Learning Methodology:
- ✅ Research docs, extract facts
- ✅ Store in Graphiti knowledge graph
- ✅ Create knowledge base files in `memory/knowledge/`
- ✅ Document EventVikings-specific use cases
- ✅ Compare technologies (Kamailio vs OpenSIPS)
- ✅ Identify integration patterns

### Progress Tracking:
```
[✓] Kamailio        - 2026-03-17 13:45-14:20 (35 min)
[ ] OpenSIPS        - TBD
[ ] FreeSWITCH      - TBD
[ ] HAProxy         - TBD
[ ] Fail2Ban        - TBD
[ ] React           - TBD
```

### Resources Collected:
- Kamailio docs: ✅ official, minimal config, FreeSWITCH integration
- FreeSWITCH docs: ✅ SignalWire docs, codecs, commercial modules
- OpenSIPS docs: ✅ manual, modules list, recent releases
- HAProxy docs: ✅ config manual, performance, security patches

### Next Actions:
1. Continue OpenSIPS research (next carrier-grade SIP proxy)
2. Create EventVikings-specific configs for all technologies
3. Map integration patterns: Kamailio → FreeSWITCH, HAProxy load balancing
4. Document security best practices (Fail2Ban integration)
5. Consider React dashboard for monitoring and management

---

**Learning Session Started:** 2026-03-17 13:45 MST  
**Time Budget:** Flexible, aim for 2-3 hours per technology  
**Status:** Phase 1 Complete (Kamailio) → Moving to Phase 2 (OpenSIPS)
