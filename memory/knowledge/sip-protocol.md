# CB Knowledge: SIP Protocol (Session Initiation Protocol)

Proficiency: **aware** (updated 2026-03-21)
Last Studied: **2026-03-21**

---

## What is SIP?

**SIP (Session Initiation Protocol)** is a signaling protocol designed to create, modify, and terminate multimedia sessions over IP networks. It's the foundation of VoIP calling and is critical for EventVikings predictive dialer functionality.

### Core Purpose

SIP is an **application layer control protocol** that:
- Creates, modifies, and terminates two-party or multiparty sessions
- Supports voice, video, and multimedia calls
- Works alongside other protocols (RTP for media, SDP for session parameters)

### Protocol Characteristics

- **Request/Response Model:** Similar to HTTP/SMTP
- **Ports:** UDP/TCP on **5060** (standard), **5061** (TLS/secured)
- **Session Types:** Unicast (2-party) or multicast (multiparty)
- **Media Transport:** RTP (Real-time Transport Protocol) carries actual voice/video
- **Session Description:** SDP (Session Description Protocol) negotiates media parameters

---

## SIP Call Flow: 5 Core Functions

### 1. **User Location**
Determines where the end system is that will be used for a call.

### 2. **User Availability**
Determines willingness/availability of called party to engage in a call.

### 3. **User Capabilities**
Determines media and parameters (codecs, ports) for the call.

### 4. **Session Setup**
Establishes session parameters from both parties (ringing).

### 5. **Session Management**
Invokes services including transfer, termination, and modifying session parameters.

---

## SIP Message Structure

### Request Methods (Methods)

| Method | Purpose |
|--------|---------|
| **INVITE** | Initiate a session |
| **ACK** | Confirm final response to INVITE |
| **BYE** | Terminate a session |
| **CANCEL** | Cancel a pending request |
| **REGISTER** | Register user location with SIP server |
| **OPTIONS** | Query server capabilities |
| **UPDATE** | Modify session parameters |
| **INFO** | Send mid-call signaling |
| **MESSAGE** | Instant messaging |

### SIP Request Example

```sip
INVITE sip:user@sipserver.com SIP/2.0
Via: SIP/2.0/UDP 10.10.10.10:5060
From: "Me" <sip:me@sipserver.org>;tag=a0
To: "User" <sip:user@sipserver.org>
Call-ID: d@10.10.10.10
CSeq: 1 INVITE
Contact: <sip:10.10.10.10:5060>
User-Agent: SIPTelephone
Content-Type: application/sdp
Content-Length: 251

v=0
o=audio1 0 0 IN IP4 10.10.10.10
s=session
c=IN IP4 10.10.10.10
m=audio 54742 RTP/AVP 4 3
a=rtpmap:4 G729/8000
a=rtpmap:3 GSM/8000
```

### Response Codes

| Code | Description |
|------|-------------|
| **1xx** | Provisional (Ring, Connecting) |
| **200 OK** | Request successful |
| **3xx** | Redirection (Moved elsewhere) |
| **4xx** | Client Error (404 Not Found, 403 Forbidden) |
| **5xx** | Server Error (503 Service Unavailable) |
| **6xx** | Global Failure |

---

## SIP Components (Architecture)

### User Agents (UA)

**User Agent Client (UAC)** - Initiates requests
- SIP Phone, softphone, predictive dialer

**User Agent Server (UAS)** - Responds to requests
- SIP Server, PBX, call manager

### SIP Servers

1. **Registrar Server**
   - Accepts REGISTER requests
   - Maps user addresses to IP addresses
   - Maintains location database

2. **Proxy Server**
   - Forwards requests on behalf of clients
   - Can enforce policy, authentication
   - Load balancing, routing decisions

3. **Redirect Server**
   - Returns 3xx responses with alternative addresses
   - Client contacts alternative endpoint

4. **Location Server**
   - Database for registrar
   - Stores user location mappings

---

## Session Description Protocol (SDP)

SDP negotiates session parameters within SIP messages:

```sdp
v=0              # Protocol version
o=sessionid sessionver IPaddr platform
s=session name
i=session description
u=URI of session info
e=email of contact
c=connection information (IP address)
t=startTime endTime
m=media (audio/video) port protocol format
a=attributes (codecs, encryption, etc.)
```

### Example SDP Body

```sdp
v=0
o=alice 2890844526 2890844526 IN IP4 host.example.com
s=Call from Alice
c=IN IP4 192.0.2.1
t=0 0
m=audio 49170 RTP/AVP 0
a=rtpmap:0 PCMU/8000
m=video 51372 RTP/AVP 31
a=rtpmap:31 H261/90000
```

---

## SIP in EventVikings Predictive Dialer Context

### Predictive Dialing Architecture

1. **Predictive Dialer (UAC)** - Initiates calls
2. **SIP Trunk Provider** - Connects to PSTN
3. **PBX/VoIP System** - Manages call routing
4. **Agents** - Handle answered calls

### SIP Messages in Predictive Dialer

**Call Initiation Flow:**
```
Predictive Dialer (UAC) → SIP INVITE → SIP Server → PSTN Gateway
PSTN Gateway → 180 Ringing → Predictive Dialer
PSTN → Agent Answers → SIP ACK → Call Connected
```

**Key SIP Operations:**
- **REGISTER** - Dialer registers with SIP trunk provider
- **INVITE** - Initiate outbound call to PSTN
- **180/183 Ringing** - Call progressing notifications
- **200 OK** - Remote party answered
- **ACK** - Confirm call establishment
- **BYE** - End call after agent terminates

### Integration Points with FreeSWITCH

FreeSWITCH as SIP server handles:
- **Call routing** - Determines where to route calls
- **Registration management** - Tracks SIP endpoints
- **Media negotiation** - SDP codec selection (G729, PCMU, GSM, etc.)
- **Transfer/hold** - Call control features

---

## SIP Trunking

SIP Trunking replaces traditional phone lines:

**Traditional vs SIP:**
- **PRI Lines:** 23 voice channels, TDM, expensive
- **SIP Trunk:** Unlimited channels, packet-based, cost-effective

**Benefits:**
- Scalable (add channels as needed)
- Cost reduction (lower长途 rates)
- Geographic flexibility (local numbers anywhere)
- Unified voice/data infrastructure

---

## Security Considerations

### Common Security Issues

1. **Toll Fraud** - Unauthorized calls (requires auth)
2. **Eavesdropping** - SIP/RTP interception
3. **Denial of Service** - SIP flood attacks

### SIP Security Best Practices

1. **Authentication** - SIP digest auth, certificates
2. **Encryption:**
   - **SIPS** - SIP over TLS (port 5061)
   - **SRTP** - Secure RTP for media encryption
3. **Firewall/NAT Traversal:**
   - **STUN** - Discover public IP
   - **TURN** - Relay for NAT
   - **ICE** - Combined solution
4. **Rate Limiting** - Prevent flood attacks
5. **Whitelisting** - Known SIP peers only

---

## SIP vs WebRTC

### SIP
- Traditional VoIP protocol
- Requires separate signaling (SIP) + media (RTP)
- NAT traversal challenges
- Legacy systems compatibility

### WebRTC
- Browser-based real-time communication
- Built-in secure signaling/data channels
- No plugins, native browser support
- Requires TURN/STUN for NAT

**EventVikings Consideration:**
- For browser-based dialer: WebRTC preferred
- For traditional integration: SIP with FreeSWITCH

---

## Common SIP Tools & Debugging

### wireshark
Packet capture and analysis:
```bash
wireshark -i eth0 -f "port 5060 or port 5061"
```

### sngrep (SIP Flow Monitor)
Real-time SIP call monitoring:
```bash
sngrep -i eth0
```

### pjsip (PJSUA)
Command-line SIP client:
```bash
pjsua --driver=pjsua2 --log-level=3
```

### sipsak (SIP Tools)
SIP message testing:
```bash
sipsak -q -s sip:server.com -d "Hello SIP"
```

### SIPp
SIP testing and load generation:
```bash
# Simulate UAC
sipp uac.xml -sf uas.xml

# Simulate UAS
sipp uas.xml
```

---

## Key Takeaways for EventVikings

1. **SIP is the protocol** - EventVikings uses SIP for call signaling
2. **FreeSWITCH handles** - Registration, routing, media negotiation
3. **SDP negotiates** - Codecs (G729, PCMU, GSM), ports (54742 typically)
4. **RTP carries media** - Voice packets after SIP session established
5. **NAT/STUN/TURN** - Critical for reliable VoIP across networks
6. **Security essential** - TLS, SRTP, authentication prevent toll fraud

---

## Learning Progress

- **Proficiency:** Awareness (knows what SIP is, basic concepts)
- **Next Level:** Basic - implement hands-on with FreeSWITCH
- **Prerequisites:** FreeSWITCH basic proficiency (achieved 2026-03-17)
- **Context:** EventVikings predictive dialer depends on SIP/FreeSWITCH integration

---

## References

- **SIP RFC 3261** - Core SIP specification
- **VoIP Mechanic** - Comprehensive SIP basics and response codes
- **Tutorialspoint** - SIP tutorial for telecom professionals
- **FreeSWITCH Documentation** - SIP server integration guide

---

## Status

- **Proficiency:** aware (updated 2026-03-21)
- **Knowledge File:** Created `memory/knowledge/sip-protocol.md`
- **Next Steps:** Hands-on with FreeSWITCH SIP configuration and NAT traversal
- **Mission Impact:** HIGH - EventVikings predictive dialer depends on SIP functionality
