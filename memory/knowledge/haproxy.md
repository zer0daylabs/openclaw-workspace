# HAProxy Learning Summary

**Date:** 2026-03-17  
**Status:** Research Complete  
**Proficiency Level:** `aware`

---

## What is HAProxy?

**HAProxy** is the **de-facto standard open-source load balancer** for TCP/HTTP applications.

**Key Stats:**
- **Current Version:** 3.4-dev6 (March 2026)
- **LTS Versions:** 3.2, 3.0, 2.8 (5-year support)
- **Performance:** 2M+ HTTP requests/sec, 100 Gbps forwarded traffic
- **Established:** 2001 (25+ years of continuous development)
- **License:** GPLv2+
- **Founder:** Willy Tarreau (principal maintainer)

**Position in Stack:**
```
EventVikings Predictive Dialer Infrastructure
├── **HAProxy** (Load Balancer) ← INFRASTRUCTURE BACKBONE
│   ├── SSL Termination
│   ├── Load Balancing
│   └── Health Checks
│
├── Kamailio (SIP Proxy)
├── OpenSIPS (SIP Proxy)
└── FreeSWITCH (Media Server)
```

---

## Core Capabilities

### Load Balancing Types
- **TCP Load Balancing:** Layer 4 (IP/Port)
- **HTTP Load Balancing:** Layer 7 (content-aware routing)
- **SSL Termination:** Offload TLS from backend
- **Health Checks:** Active and passive monitoring
- **Session Persistence:** Sticky sessions, cookie-based
- **Rate Limiting:** Connection throttling

### Protocol Support
- **HTTP/1.1, HTTP/2, HTTP/3 (QUIC)**
- **TCP:** Any TCP-based protocol
- **WebSocket:** Full duplex communication
- **gRPC:** HTTP/2 load balancing
- **PROXY Protocol:** Pass client IP through LB

### Advanced Features
- **SSL/TLS:** Full certificate management
- **ACME/Let's Encrypt:** Automatic certificate renewal
- **JSON/CBOR logging:** Structured logging formats
- **Lua scripting:** Custom logic at LB layer
- **Kernel TLS (KTLS):** Offload SSL to kernel
- **TLS ECH:** Encrypted client Hello
- **QUIC:** HTTP/3 support

---

## HAProxy Versions (2026)

### Current Releases:
- **3.4-dev6** (2026-03-05) - Development branch
- **3.3.5** (2026-03-09) - Stable (EOL 2027-Q1)
- **3.2.14** (2026-03-09) - LTS (EOL 2030-Q2) ← Recommended
- **3.0.18** (2026-03-09) - LTS (EOL 2029-Q2)
- **2.8.19** (2026-03-09) - LTS (EOL 2028-Q2)

### Version Strategy:
- **Even numbers:** LTS (5 years support)
- **Odd numbers:** Stable (12-18 months support)
- **Annual releases:** Q1 and Q3 major releases
- **Weekly patches:** Critical fixes

---

## HAProxy in EventVikings Architecture

### Load Balancing Kamailio/OpenSIPS:

```haproxy
# HAProxy Configuration for Kamailio
frontend kamailio_front
    bind *:5060 proto=udp
    
    # Stats page
    stats enable
    stats uri /stats
    stats refresh 10s
    
    # Forward to Kamailio cluster
    use_backend kamailio_back

backend kamailio_back
    balance roundrobin
    option tcp-check
    
    # Kamailio instances
    server kamailio-1 192.168.0.101:5060 check inter 2s fall 3 rise 2
    server kamailio-2 192.168.0.102:5060 check inter 2s fall 3 rise 2
    server kamailio-3 192.168.0.103:5060 check inter 2s fall 3 rise 2

    # Health check
    tcp-check send Sip\r\n
    tcp-check expect string 200
```

### SSL Termination for Web Applications:
```haproxy
frontend web_https
    bind *:443 ssl crt /etc/ssl/certs/web.pem
    
    # ACME automatic certificate
    http-use-ssl-filters acme
    
    # Health check
    acl is_health_check path_beg /health
    
    # Route to web servers
    use_backend web_servers if !is_health_check

backend web_servers
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    
    server web-1 192.168.0.20:80 check
    server web-2 192.168.0.21:80 check
    server web-3 192.168.0.22:80 check
```

---

## HAProxy Performance Characteristics

### Performance Features:
- **Event-driven:** Reacts to I/O events instantly
- **Multi-threaded:** SMP parallelism, thread groups
- **Zero-copy:** Direct file forwarding
- **Kernel TLS:** Hardware acceleration
- **CPU Binding:** Pin to specific cores
- **Dynamic Scaling:** Add/remove servers without restart

### Benchmark Results (AWS Graviton2):
- **HTTP over SSL:** 2M+ requests/sec
- **Forwarded traffic:** 100 Gbps
- **Latency:** Sub-millisecond at scale
- **Scalability:** Linear scaling with cores

### Scalability:
```bash
# HAProxy scales horizontally
# Example: 16 cores
thread-max 16
tune.spread 16

# Thread groups
tune.tlsv13group 4
```

---

## HAProxy Integration Patterns

### Pattern 1: Kamailio Load Balancer
```
External SIP Trunk
       ↓
  HAProxy (UDP:5060)
       ↓
┌─────┴─────┴─────┐
│ Kamailio-1    │ Kamailio-2  │ Kamailio-3
└─────┬─────┬─────┘
      │     │
  FreeSWITCH Cluster
```

### Pattern 2: HAProxy Proxy Protocol (OpenSIPS 4.0+)
```haproxy
# Enable PROXY protocol on frontend
frontend sip_front
    bind *:5060 proto=tcp
    option proxy-protocol v2
    
    use_backend opensips_back

backend opensips_back
    server opensips-1 192.168.0.101:5060 proxy-v2-check
```

### Pattern 3: SSL Termination + Internal TLS
```
Client → HAProxy (HTTPS)
        ↓ TLS Termination
    Internal Traffic (HTTP/TCP)
        ↓ Encryption
    Backend → TLS (end-to-end)
```

### Pattern 4: Rate Limiting
```haproxy
frontend sip_limit
    bind *:5060
    
    # Rate limiting based on source IP
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 100 }
```

---

## HAProxy Configuration Structure

### Core Sections:
1. **global** - Global parameters
2. **defaults** - Default settings for all
3. **frontend** - Entry points (ports, ACLs)
4. **backend** - Server pools, load balancing
5. **listen** - Combined frontend+backend
6. **resolvers** - DNS resolution
7. **backend-ssl** - SSL termination

### Configuration Example:
```haproxy
global
    log /dev/log local0
    maxconn 4096
    thread-stack-size 384
    tune.ssl.default-dh-param 2048
    
    # Performance
    tune.http.max-header-field-size 8KB
    tune.ssl.largest-fragment 16KB
    
    # CPU binding
    cpu-map 1-8 0-7

defaults
    mode tcp
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option dontlognull

frontend kamailio_front
    bind *:5060 proto=udp
    stats enable
    stats uri /stats
    
    use_backend kamailio_back

backend kamailio_back
    balance roundrobin
    option tcp-check
    server kamailio-1 192.168.0.101:5060 check
```

---

## HAProxy Monitoring

### Built-in Stats Page:
- **URI:** `/stats` (basic auth required)
- **Refresh:** Configurable polling
- **Export:** Prometheus metrics endpoint
- **Graphs:** Response times, connection counts

### Prometheus Export:
```haproxy
global
    stats exporter

gauges
    my.custom_metric gauge
```

### Log Format:
```bash
# Custom log format
log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Ttim %Tw/%Tc/%Tr -- %ST %B %CC %CS %tsc %ac/%fc/%sc/%rc %sq/%bq %hr %hs %tr %{+Q}r"
```

---

## Security Features

### TLS/SSL Hardening:
```haproxy
# Minimum TLS version
tls-min-tlsv12

# Cipher suites
ssl-default-bind-ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384

# DH parameters
ssl-default-bind-options no-sslv3 no-tlsv10 no-tlsv11

# OCSP Stapling
ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
```

### Attack Prevention:
- **SYN Flood:** `option synproxy` (kernel support)
- **Slowloris:** `timeout client connect` limits
- **HTTP Slow Attack:** `tune.http.max hdr` limits
- **DDoS:** Rate limiting, IP whitelisting
- **SQL Injection:** ACLs, input validation

---

## HAProxy vs NGINX

| Feature | HAProxy | NGINX |
|--|--|--|
| **Primary Role** | Load balancer | Web server/LB |
| **TCP LB** | Excellent | Good (paid) |
| **HTTP LB** | Excellent | Excellent |
| **Performance** | Higher throughput | Lower latency |
| **Configuration** | Simple, declarative | Complex, modular |
| **Lua** | Built-in | Via OpenResty |
| **SSL** | Native | Excellent |
| **QUIC** | Native | Native |
| **Cost** | Free (GPL) | Free (Apache 2) |

**Recommendation:** HAProxy for pure load balancing, NGINX for web serving + LB

---

## Learning Status

### ✅ Knowledge Captured:
- HAProxy architecture and performance characteristics
- Version strategy and releases (3.4-dev, 3.2 LTS)
- EventVikings integration patterns
- Kamailio/OpenSIPS load balancing
- SSL termination and ACME integration
- Monitoring and observability
- Security hardening best practices

### 📚 Documentation Links:
- **Manual:** http://docs.haproxy.org/
- **Intro:** http://docs.haproxy.org/dev/intro.html
- **Git:** https://github.com/haproxy/haproxy
- **Demo:** http://demo.haproxy.org/
- **Enterprise:** https://www.haproxy.com/
- **Slack:** https://slack.haproxy.org/

### 🔄 Graphiti Storage:
- HAProxy overview and features
- Version strategy (LTS vs stable)
- EventVikings load balancing patterns
- Kamailio integration configs
- Monitoring and security

---

## Next Steps for EventVikings

1. ✅ HAProxy research complete
2. 🎯 Plan load balancer architecture
3. 🔧 Design Kamailio cluster topology
4. 🔐 Configure SSL termination
5. 📊 Set up monitoring and alerting
6. 🚀 Deploy and test failover

**Recommendation:** HAProxy is ideal for EventVikings - proven carrier-grade reliability, excellent Kamailio integration, and built-in monitoring for production operations.

---

**Knowledge stored in:** `~/.openclaw/workspace/memory/knowledge/haproxy.md`  
**Learning session:** 2026-03-17 14:35 MST  
**Duration:** ~20 minutes
