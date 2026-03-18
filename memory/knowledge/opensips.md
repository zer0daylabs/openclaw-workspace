# OpenSIPS Learning Summary

**Date:** 2026-03-17  
**Status:** Phase 2 Complete  
**Proficiency Level:** `aware`

---

## What is OpenSIPS?

**OpenSIPS** is a **multi-functional, high-throughput SIP server** used by carriers, telecoms, and ITSPs for enterprise/VoIP solutions.

**Key Stats:**
- **Throughput:** 10K+ call setups/sec (stateless load balancer mode)
- **Scale:** 300K+ online subscribers on 4GB RAM
- **Modules:** 70+ included modules
- **Versions:** 3.6.4, 3.4.17 (LTS stable)
- **License:** Open Source (GPL)

**History:**
- **Started:** ~2003 (similar era to Kamailio/SER)
- **Security Audit:** 3.2 version audited (2022)
- **Active Development:** 4.0 in progress (March 2026)

---

## Core Capabilities

### SIP Server Functions
- **Registrar server** - User registration and location
- **Location server** - Track subscriber endpoints
- **Proxy server** - Forward SIP requests (stateful/stateless)
- **Redirect server** - Redirect requests to alternate locations
- **Routing engine** - Flexible, powerful scripting language

### Transport Support
- **Protocols:** UDP, TCP, TLS, SCTP
- **IP versions:** IPv4, IPv6
- **DNS:** SRV, NAPTR records, SRV failover
- **Multi-homed:** Support for complex network topologies
- **Multi-domain:** Host multiple domains on single server

### Features
- **Security:** IP Blacklists, digest auth, IP auth
- **AAA:** Authentication, Authorization, Accounting via SQL/RADIUS/DIAMETER
- **NAT Traversal:** SIP and RTP NAT handling
- **Presence:** Presence Agent with XCAP support
- **CPL:** Call Processing Language (RFC3880)
- **ENUM:** E.164 Number Mapping support
- **Load Balancing:** With failover capabilities
- **Least Cost Routing:** Optimize call costs
- **Dialog Support:** Call monitoring, termination, profiling
- **Gateway:** SMS gateway (AT-based), PSTN interconnection
- **XMPP Gateway:** Server-to-server translation

### Database Backends
- MySQL, PostgreSQL, Oracle, Berkeley DB
- Text files, ODBC-compatible databases
- Flat files for lightweight deployments

### Management Interfaces
- **FIFO file** - Runtime control
- **Unix sockets** - Local management
- **XMLRPC** - Remote integration
- **Datagram** (UDP/unixsockets)
- **SNMP** - Network monitoring

### Custom Extensions
- **PERL Interface** - Embed Perl extensions
- **Java SIP Servlet** - Write Java SIP Servlets
- **Lua scripting** (via modules)
- **Plug-and-play modules** - No core changes needed

---

## Scalability Performance

### Benchmark Capabilities:
```
Minimum Configuration:
- Embedded systems, limited resources
- ~100-200 call setups/sec
- 300K+ subscribers on 4GB RAM

Load Balancer Mode (stateless):
- 5,000+ call setups/sec
- Multiple servers scale horizontally
- Geographic distributed platforms

Enterprise Deployment:
- Carrier-grade scalability
- Geographic redundancy
- Failover and clustering
```

---

## Recent Developments (2026)

### OpenSIPS 4.0 Features (Current Dev):
1. **Bond Sockets** (March 2026)
   - DNS-based destination selection
   - Protocol/address family discovery
   - Proper outbound socket selection

2. **Proxy Protocol Support** (Feb 2026)
   - HAProxy integration
   - Preserve client IP information
   - TCP load balancer support

3. **Big Scaling SIP Forking** (Feb 2026)
   - Dynamic branch allocation
   - No memory/processing penalties
   - High-scale forking scenarios

4. **Config Module** (May 2025)
   - Runtime configuration tuning
   - No restart needed
   - Dynamic parameter updates

5. **Unified SIP Branches** (May 2025)
   - Pre/post relaying correlation
   - Custom branch data attachment
   - Inter-branch data access

6. **Structured SDP Manipulation** (May 2025)
   - Real-time SDP editing
   - Access and replace media parameters
   - SDP body manipulation

7. **Sockets Management** (May 2025)
   - Runtime socket configuration
   - Dynamic SIP socket management
   - Configuration module integration

### Current Stable Releases:
- **3.6.4** (LTS) - Current stable
- **3.4.17** (LTS) - Extended support
- Both actively patched with security updates

---

## OpenSIPS vs Kamailio Comparison

| Feature | Kamailio | OpenSIPS |
|---------|----------|----------|
| **Performance** | 10K+ CPS | 5K+ CPS (stateless) |
| **Modules** | 100+ | 70+ |
| **Configuration** | Flexible scripting | Powerful scripting |
| **Focus** | Carrier-grade flexibility | Carrier-grade scale |
| **Recent** | v6.1.0 (Feb 2026) | v3.6.4 (LTS), 4.0 dev |
| **HAProxy** | Integration via custom config | Built-in Proxy Protocol support |
| **Runtime Config** | Config module (3.6) | Config module (3.6) |
| **Security** | Audited 3.2 (2022) | Audited 3.2 (2022) |

### Similarities:
- Both carrier-grade SIP proxies
- Config-driven routing logic
- Extensive module ecosystems
- SQL database backends
- Similar scripting languages (both use pseudo-variables)
- Both support TLS, TCP, SCTP transports

### Key Differences:
- **Kamailio:** More modular, better documented, more flexible routing
- **OpenSIPS:** Stronger in carrier deployments, Java/Perl extensibility
- **Module System:** Kamailio more granular, OpenSIPS more integrated

---

## EventVikings Application

### Current Architecture:
```
SIP Trunk → Kamailio → FreeSWITCH → Agents/PBX
```

### OpenSIPS as Kamailio Alternative:
```
SIP Trunk → OpenSIPS → FreeSWITCH → Agents/PBX
```

### Why Consider OpenSIPS:
- **If you prefer:** Carrier-grade deployments, Java/Perl extensions
- **For scale:** Similar performance, proven at enterprise level
- **Migration:** Config syntax similar, module migration required

### Recommended Use Case:
- **Keep Kamailio** if you've invested in Kamailio expertise
- **Consider OpenSIPS** if:
  - Need Java SIP Servlet integration
  - Prefer Perl extensions
  - Carrier deployment with specific requirements
  - Need built-in HAProxy Proxy Protocol support

---

## Key Modules for EventVikings

### Essential Modules:
- `tm` - Transaction management
- `sl` - Simple Reply
- `rr` - Record Route
- `pv` - Pseudo Variables
- `maxfwd` - Max-Forward header
- `textops` - Text manipulation
- `siputils` - SIP utilities
- `xlog` - Extended logging

### Database Modules:
- `db_mysql` or `db_postgres` - SQL operations
- `db_berkeley` - Lightweight storage

### Security Modules:
- `auth` - Authentication
- `acc` - Accounting
- `dispatcher` - Load balancing
- `htable` - Hash table storage
- `ipops` - IP manipulation

### Advanced Modules:
- `presence` - Presence server
- `xcap` - XCAP server
- `cpl` - Call processing language
- `nathelper` - NAT traversal
- `dialog` - Call monitoring

---

## Learning Status

### ✅ Knowledge Captured:
- Core capabilities and architecture
- Performance benchmarks
- 2026 feature releases
- Comparison with Kamailio
- EventVikings application patterns

### 📚 Documentation Links:
- **Manuals:** https://www.opensips.org/Documentation/Manuals
- **Modules List:** https://www.opensips.org/Documentation/Modules-3-4
- **Tutorials:** https://www.opensips.org/Documentation/Tutorials
- **Community:** https://www.opensips.org/Community/OpenSIPS-CE

### 🔄 Graphiti Storage:
- Core facts about OpenSIPS capabilities
- Performance benchmarks
- 2026 feature releases
- Kamailio vs OpenSIPS comparison
- EventVikings integration patterns

---

## Next Steps

1. ✅ OpenSIPS research complete (knowledge base: 7KB+)
2. 📝 Document EventVikings-specific OpenSIPS config pattern
3. 📊 Compare actual deployment requirements
4. 🎯 Decide: Stick with Kamailio or evaluate OpenSIPS migration

**Recommendation:** Stay with Kamailio for EventVikings unless specific requirements favor OpenSIPS features (Java/Perl extensions, HAProxy Proxy Protocol).

---

**Knowledge stored in:** `~/.openclaw/workspace/memory/knowledge/opensips.md`  
**Learning session:** 2026-03-17 14:20 MST  
**Duration:** ~20 minutes

