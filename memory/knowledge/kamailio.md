# Kamailio Learning Summary

**Date:** 2026-03-17  
**Status:** Phase 1 Complete  
**Proficiency Level:** `aware`

---

## What is Kamailio?

**Kamailio** (formerly OpenSER, then SER before trademark) is the **open source SIP server** for carrier-grade real-time communications.

- **Performance:** Handles **thousands of call setups per second**
- **Language:** Pure C for Unix/Linux with architecture-specific optimizations
- **License:** GPLv2+
- **History:** Started 2001 as SIP Express Router (SER) at FhG Fokus Berlin, merged back with SER in 2008, renamed to Kamailio in 2008

---

## Core Capabilities

### SIP Routing & Proxy Functions
- **SIP proxy server** (stateful and stateless modes)
- **Load balancer** for SIP endpoints/media servers
- **Least cost routing** and DID routing
- **SIP firewall** and edge proxy
- **SBC (Session Border Controller)**
- **Registrar and location service**
- **IMS/VoLTE extensions**
- **ENUM** routing
- **Failover and routing policies**

### Real-Time Communication Services
- **Presence and instant messaging** (SIMPLE)
- **MSRP relay** with embedded XCAP server
- **WebRTC support** (WebSocket, WSS)
- **RTP proxy integration** for media relay
- **Accounting** and **authorization**

### Transport & Protocol Support
- **UDP, TCP, TLS, SCTP** transports
- **IPv4 and IPv6** dual-stack
- **WebRTC** via WebSocket (WS/WSS)
- **Secure VoIP** with TLS encryption

### Database Backends
- MySQL, PostgreSQL, Oracle, RADIUS
- LDAP, Redis, Cassandra, MongoDB, Memcached

### Control Interfaces
- **JSON-RPC / XML-RPC** remote control
- **MI (Management Interface)** FIFO/Unix socket
- **SNMP monitoring**
- **kamcmd/kamctl** CLI tools

---

## Architecture Pattern for Predictive Dialers

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ SIP Trunk       │─────▶│ Kamailio Proxy  │─────▶│ FreeSWITCH      │
│ (Provider)      │      │ (Load Balancer) │      │ (Media Server)  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
         │                                                       │
         ▼                                                       ▼
   Auth/Trunk handling                              Call processing,
   Routing logic                                    IVR, Recording
```

### Kamailio's Role
- Receives INVITEs from SIP trunk/provider
- Performs authentication (username/password from trunk)
- Strips authentication requirements for internal PBX
- Load balances across multiple FreeSWITCH servers
- Number pattern matching and routing
- Anti-fraud filtering

### FreeSWITCH's Role
- Media handling (RTP streams)
- IVR and call flows
- Recording and analytics
- Agent queue management for predictive dialing

---

## Configuration Structure

Kamailio config file (`kamailio.cfg`) has **3 sections**:

### 1. Global Parameters
```ini
fork=yes
children=4
log_facility=LOG_LOCAL0
disable_tcp=yes
listen=udp:192.168.0.101:5060
port=5060
mpath="/usr/lib/kamailio/modules/"
```

### 2. Module Loading & Settings
```ini
loadmodule "mi_fifo.so"
loadmodule "tm.so"
loadmodule "sl.so"
loadmodule "rr.so"
loadmodule "pv.so"
loadmodule "maxfwd.so"
loadmodule "textops.so"
loadmodule "siputils.so"
loadmodule "xlog.so"

modparam("mi_fifo", "fifo_name", "/tmp/kamailio_fifo")
```

### 3. Routing Blocks
```ini
route{
    # Check max-forward header
    if (!mf_process_maxfwd_header("10")) {
        sl_send_reply("483","Too Many Hops");
        break;
    }
    
    # Process initial INVITE
    if (method=="INVITE") {
        record_route();
        # SQL lookup for number→destination mapping
        if (subst_user('/^\+?1?([0-9]{10})$/1\1/')) {
            sql_query("ca", "SELECT accountcode FROM numbers WHERE number = '$rU'", "ra");
            $var(hp) = $dbr(ra=>[0,0]);
        }
    } else {
        sl_send_reply("404","Not here");
        exit;
    }
    
    # Forward to appropriate destination
    if ($var(hp) == 0) {
        sl_send_reply("404","Not here");
        exit;
    } else {
        rewritehostport("192.168.0.102:5060");
    }
    
    # Relay
    if (!t_relay()) {
        sl_reply_error();
    }
}
```

---

## Key Modules for Predictive Dialer Use

### Essential Modules
- `tm` - Transaction management
- `sl` - Simple Reply
- `rr` - Record Route
- `pv` - Pseudo Variables
- `maxfwd` - Max-Forward header processing
- `textops` - Text manipulation functions
- `siputils` - SIP utility functions
- `xlog` - Extended logging

### Database Modules (for number routing)
- `db_postgres` or `db_mysql` - SQL backend
- `sqlops` - SQL operations in config

### Optional for Production
- `auth_db` - User authentication
- `usrloc` - User location database
- `nat_traversal` - NAT/Firewall handling
- `dialplan` - Advanced dial plans
- `registrar` - SIP registration
- `alias_db` - Alias lookups

---

## FreeSWITCH Integration Pattern

### Basic Proxy Setup
```ini
# Listen for SIP from provider
listen=udp:192.168.0.101:5060

# Forward all matched INVITEs to FreeSWITCH
rewritehostport("192.168.0.102:5060")
```

### SQL-Based Routing
```ini
# Match 10-11 digit numbers
if (subst_user('/^\+?1?([0-9]{10})$/1\1/')) {
    sql_query("ca", "SELECT destination FROM routing WHERE number = '$rU'", "ra");
    $var(dest) = $dbr(ra=>[0,0]);
}

# Multi-destination load balancing
switch ($var(dest)) {
    case 1:
        rewritehostport("192.168.0.102:5060");
        break;
    case 2:
        rewritehostport("192.168.0.103:5060");
        break;
}
```

---

## Learning Notes

### Strengths
- ✅ Carrier-grade performance (10K+ call setups/sec)
- ✅ Highly modular - load only what you need
- ✅ Flexible routing logic via config scripting
- ✅ Extensive database backend support
- ✅ Actively maintained (v6.1.0 released Feb 2026)

### Considerations
- ⚠️ Config syntax has learning curve
- ⚠️ Debugging requires understanding SIP message flow
- ⚠️ Production setup needs careful testing (start with minimal config)
- ⚠️ Network topology awareness (NAT/Firewall patterns)

### Recommended Next Steps
1. **Start with minimal config** - use example from GitHub
2. **Test locally first** - use kamailio-minimal-proxy.cfg
3. **Gradually add modules** - tm, sl, rr first, then DB modules
4. **Monitor with kamcmd** - use MI FIFO for runtime stats
5. **Set up logging** - syslog with LOG_LOCAL0 for production

---

## Resources

- **Official docs:** https://www.kamailio.org/w/
- **Minimal config example:** https://github.com/kamailio/kamailio/blob/master/misc/examples/mixed/kamailio-minimal-proxy.cfg
- **FreeSWITCH integration guide:** SignalWire docs (linked above)
- **Core cookbook:** https://www.kamailio.org/wikidocs/cookbooks/5.2.x/core/
- **Latest release:** v6.1.0 (Feb 18, 2026)

---

**Knowledge stored in Graphiti:** 5 facts on Kamailio core, capabilities, EventVikings integration, config structure, FreeSWITCH pattern.

**Status:** Ready to apply Kamailio knowledge to EventVikings predictive dialer system.
