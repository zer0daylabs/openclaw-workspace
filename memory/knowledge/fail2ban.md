# Fail2Ban Learning Summary

**Date:** 2026-03-17  
**Status:** Research Complete  
**Proficiency Level:** `aware`

---

## What is Fail2Ban?

**Fail2Ban** is a **Python-based intrusion prevention framework (IPS)** that protects servers from brute-force attacks and malicious behavior.

**Key Stats:**
- **Language:** Python 3.x
- **License:** GPLv2+
- **Active Development:** Yes, regular updates
- **Integration:** iptables, firewalld, IPsets, custom actions
- **Platform:** Linux (any Unix-like system)

**Position in Stack:**
```
EventVikings Predictive Dialer - Security Layer
├── Kamailio (SIP Proxy)
├── FreeSWITCH (Media Server)
└── **Fail2Ban** (Intrusion Prevention) ← SECURITY LAYER
    ├── Brute Force Prevention
    ├── Flood Protection
    └── Log Monitoring
```

---

## Core Features

### Protection Mechanisms
- **Log File Monitoring:** Monitor multiple log files simultaneously
- **Regular Expressions:** Pattern matching for malicious activity
- **Ban Actions:** iptables, firewalld, IPsets, custom scripts
- **Time Windows:** Temporary bans with exponential backoff
- **Recidive Jail:** Long-term bans for repeat offenders

### Supported Services (Built-in Jails)
- **SSH:** `fail2ban-sshd` - SSH brute force protection
- **Apache/Nginx:** `fail2ban-httpd` - Web attacks
- **Postfix/Dovecot:** `fail2ban-mail` - Email abuse
- **SIP/VoIP:** `fail2ban-sip` - SIP flood attacks
- **Kamailio:** `fail2ban-kamailio` - Kamailio-specific
- **FreeSWITCH:** `fail2ban-freeswitch` - SIP attacks
- **Generic:** `fail2ban-generic` - Custom patterns

### Ban Mechanisms
```python
# Action types:
- iptables: Traditional firewall rules
- firewalld: D-Bus firewalld integration
- IPsets: Fast IP set management
- PF: OpenBSD packet filter
- nftables: Modern firewall (Linux)
- custom: User-defined scripts

# Ban durations:
- ban_time: How long to ban (600s default)
- find_time: How far back to look (600s default)
- maxretry: Max failures before ban (5 default)
- bantime_multiplier: Exponential backoff
```

---

## Fail2Ban in EventVikings Architecture

### SIP Flood Protection:

```ini
# /etc/fail2ban/jail.local

[sip-flood]
enabled = true
filter = sip-flood
action = iptables-allports[name=SIP]
logpath = /var/log/kamailio/kamailio.log
maxretry = 3
bantime = 3600
findtime = 600
```

### Kamailio Integration:

**Filter Pattern (sip-flood.conf):**
```ini
[Definition]
failregex = ^<HOST>.*[Ss]yntax error|failed to parse SIP message|^<HOST>.*SIP message too large|^<HOST>.*authentication failure
ignoreregex =
```

**Kamailio Logging:**
```ini
# kamailio.cfg
xlog("L_ERR", "SIP flood from $si\n")
```

### FreeSWITCH Integration:
```ini
[freeSWITCH]
enabled = true
filter = freeswitch
action = iptables[name=Freeswitch]
logpath = /var/log/freeswitch/freeswitch.log
maxretry = 5
bantime = 3600
findtime = 600
```

### Combined Security Stack:
```
External Traffic
    ↓
HAProxy (Rate Limiting)
    ↓
Fail2Ban (IP Bans)
    ↓
Kamailio (SIP Proxy)
    ↓
FreeSWITCH (Media Server)
```

---

## Fail2Ban Configuration

### Core Configuration Files:
1. **/etc/fail2ban/fail2ban.conf** - Main settings
2. **/etc/fail2ban/jail.conf** - Default jails
3. **/etc/fail2ban/jail.local** - Local overrides
4. **/etc/fail2ban/filter.d/** - Custom filters
5. **/etc/fail2ban/action.d/** - Custom actions

### fail2ban.conf Example:
```ini
[FAIL2BAN]
loglevel = INFO
logpath = /var/log/fail2ban.log
maxretry = 5
bantime = 3600
findtime = 600
backend = auto
purgeoldlines = true

# Actions
sender = fail2ban@localhost
sendername = Fail2Ban
milter = /var/run/fail2ban/fail2ban.sock
protocol = udp
```

### jail.local Example:
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
relog_interval = 60

# SSH Protection
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400

# Kamailio SIP Protection
[kamailio-sip]
enabled = true
filter = kamailio
port = 5060
logpath = /var/log/kamailio/kamailio.log
maxretry = 3
bantime = 3600
findtime = 300

# Web Application Protection
[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 3600
```

---

## Custom Filter Development

### Filter Structure:
```ini
[Definition]
failregex = <HOST>[\s]+([Ss]yntax error|[Ff]ailed|[Aa]uthentication error)
ignoreregex =
```

### Advanced Patterns:
```ini
# SIP authentication failure
failregex = ^<HOST>.*SIP authentication failure.*user.*<USER>

# SIP message too large
failregex = ^<HOST>.*message too large.*len=(?P<LEN>\d+)

# SIP syntax error
failregex = ^<HOST>.*[Ss]yntax error.*at.*<LINE>

# SIP flood
failregex = ^<HOST>.*INVITE.*frequency.*limit
```

### Custom Filter Example (kamailio-filter):
```ini
[Definition]
# SIP authentication failures
failregex = ^.*authentication failure.*user=[^\s]+.*srcip=<HOST>
failregex = ^.*SIP authentication failed.*srcip=<HOST>

# SIP flood detection
failregex = ^.*rate limit exceeded.*srcip=<HOST>
failregex = ^.*too many requests.*srcip=<HOST>

# SIP syntax errors
failregex = ^.*[Ss]yntax error.*srcip=<HOST>
failregex = ^.*parse error.*srcip=<HOST>

ignoreregex =
```

---

## Fail2Ban Monitoring

### Status Commands:
```bash
# Fail2Ban service status
systemctl status fail2ban

# List all jails
fail2ban-client status

# List specific jail
fail2ban-client status sshd

# List banned IPs
fail2ban-client status sshd

# Unban IP
fail2ban-client set sshd unbanip 1.2.3.4

# Ban IP manually
fail2ban-client set sshd banip 1.2.3.4
```

### Log Format:
```log
2026-03-17 14:30:00,123 fail2ban.server          [1234]: INFO    [sshd] Ban 192.168.1.100
2026-03-17 14:36:00,456 fail2ban.server          [1234]: INFO    [sshd] Unban 192.168.1.100
2026-03-17 14:45:00,789 fail2ban.filter           [1234]: WARNING [sshd] Found 192.168.1.100 - 2026-03-17 14:44:58
```

### Statistics:
```bash
# Get jail statistics
fail2ban-client status

# Monitor real-time
journalctl -u fail2ban -f

# Export stats to JSON
fail2ban-client status --json
```

---

## Fail2Ban vs Other Security Tools

### Fail2Ban vs ufw:
| Feature | Fail2Ban | ufw |
|--|--|--|
| **Purpose** | IPS (dynamic bans) | Firewall (static rules) |
| **Ban Duration** | Temporary, automatic | Manual, permanent |
| **Detection** | Log-based, patterns | Port-based |
| **Use Case** | Brute force protection | General firewall |

**Recommendation:** Use both - Fail2Ban for dynamic protection, ufw for baseline firewall.

### Fail2Ban vs CrowdSec:
- **CrowdSec:** Newer, community-driven, cloud-based threat intelligence
- **Fail2Ban:** Traditional, proven, simpler, local-only
- **Choose:** Fail2Ban for simplicity, CrowdSec for global threat sharing

### Fail2Ban vs ipset:
- **ipset:** Low-level IP set management (fast)
- **Fail2Ban:** High-level IPS framework (easy)
- **Integration:** Fail2Ban uses ipset for ban actions

---

## Fail2Ban Best Practices

### Configuration:
- ✅ Use `jail.local` (not modify `jail.conf`)
- ✅ Set appropriate `maxretry` (3-5 for SSH, 5-10 for web)
- ✅ Use reasonable `bantime` (1-24 hours for first offense)
- ✅ Enable `recidive` for repeat offenders
- ✅ Use `banaction` appropriate for your system

### Monitoring:
- ✅ Monitor Fail2Ban logs for false positives
- ✅ Check `fail2ban-client status` daily
- ✅ Review banned IPs periodically
- ✅ Set up alerting for repeated bans

### Performance:
- ✅ Use `iptables` or `nftables` (fastest)
- ✅ Avoid `recidive` jail unless needed
- ✅ Don't enable too many jails simultaneously
- ✅ Use `logpath` carefully (log rotation issues)

### Security Considerations:
- ✅ Don't ban critical IPs (your own monitoring)
- ✅ Use `whitelistip` for trusted sources
- ✅ Monitor for false positives
- ✅ Have emergency unban mechanism

---

## EventVikings Security Integration

### Recommended Fail2Ban Setup:

**Jails for Predictive Dialer:**
```ini
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400

[kamailio-sip]
enabled = true
port = 5060,5061
filter = kamailio
logpath = /var/log/kamailio/kamailio.log
maxretry = 3
bantime = 3600
findtime = 300

[freeswitch-sip]
enabled = true
port = 5060,5061
filter = freeswitch
logpath = /var/log/freeswitch/freeswitch.log
maxretry = 5
bantime = 3600

[nginx-web]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 3600

[recidive]
enabled = true
logpath = /var/log/fail2ban.log
bantime = 604800
findtime = 86400
maxretry = 3
```

### HAProxy Integration:
```ini
[haproxy-connlimit]
enabled = true
port = http,https
logpath = /var/log/haproxy.log
maxretry = 1000
bantime = 3600
```

---

## Learning Status

### ✅ Knowledge Captured:
- Fail2Ban architecture and capabilities
- SIP-specific jail configurations
- Kamailio and FreeSWITCH integration
- Custom filter development
- Monitoring and management
- Integration with other security tools

### 📚 Documentation Links:
- **Manual:** https://fail2ban.readthedocs.io/
- **GitHub:** https://github.com/fail2ban/fail2ban
- **Filters:** https://fail2ban.readthedocs.io/en/latest/filters.html
- **Actions:** https://fail2ban.readthedocs.io/en/latest/actions.html
- **Jail Config:** https://fail2ban.readthedocs.io/en/latest/configuration.html

### 🔄 Graphiti Storage:
- Fail2Ban overview and features
- Kamailio integration patterns
- FreeSWITCH SIP protection
- Custom filter development
- Monitoring and best practices

---

## Next Steps for EventVikings

1. ✅ Fail2Ban research complete
2. 🎯 Design security layer architecture
3. 🔧 Create Kamailio/FreeSWITCH filters
4. 🔐 Configure jails and ban times
5. 📊 Set up monitoring and alerting
6. 🧪 Test with simulated attacks

**Recommendation:** Fail2Ban is essential for EventVikings - protects against SIP flood attacks, brute force attempts, and provides automated defense layer.

---

**Knowledge stored in:** `~/.openclaw/workspace/memory/knowledge/fail2ban.md`  
**Learning session:** 2026-03-17 14:40 MST  
**Duration:** ~20 minutes
