# CB Knowledge: WebRTC (Web Real-Time Communication)

Proficiency: **aware** (updated 2026-03-22)
Last Studied: **2026-03-22**

---

## What is WebRTC?

**WebRTC (Web Real-Time Communication)** is a collection of APIs and protocols that enable real-time peer-to-peer communication directly between web browsers, without requiring plugins, drivers, or intermediary servers for media transfer.

### Core Capabilities

- **Audio/Video Conferencing** - Browser-based calls
- **File Exchange** - Direct file transfer between peers
- **Screen Sharing** - Share browser tabs/desktop
- **Identity Management** - Secure peer authentication
- **Legacy Integration** - PSTN gateway, DTMF signaling
- **Peer-to-Peer Data Transfer** - Arbitrary binary data

**Key Advantage:** Direct browser-to-browser connection without server-side media relaying (uses signaling server only for setup).

---

## WebRTC vs SIP (Comparison for EventVikings Context)

### SIP (Session Initiation Protocol)
- **Purpose:** Call signaling only (not media transport)
- **Transport:** RTP carries actual voice/video after SIP establishes session
- **Use Case:** Traditional VoIP, predictive dialer to PSTN
- **Server:** SIP proxy/registrars (FreeSWITCH)
- **Browser:** Not natively supported

### WebRTC
- **Purpose:** Full real-time communication (signaling + media)
- **Transport:** RTP/SCTP carries media/data directly
- **Use Case:** Browser-based communication apps
- **Server:** Signaling server (WebSocket/HTTP) for setup only
- **Browser:** Native support (Chrome, Firefox, Safari, Edge)

**EventVikings Context:**
- SIP + FreeSWITCH: Traditional predictive dialer → PSTN calls
- WebRTC: Browser-based dialer, screen sharing, live agent feedback

---

## Core WebRTC Architecture

### 1. RTCPeerConnection
**Central interface** for managing peer connections.

Key responsibilities:
- Establishes connection between two peers
- Handles ICE/STUN/TURN negotiation
- Manages media streams and data channels
- Monitors connection state

### 2. Media Streams (MediaStream)
**Captured media** from user's device.

Sources:
- **getUserMedia()** - Webcam, microphone
- **getDisplayMedia()** - Screen sharing
- **MediaStreamTrack** - Individual audio/video/text tracks

### 3. RTCDataChannel
**Bi-directional data channel** for arbitrary binary data.

Use cases:
- Real-time chat messages
- File transfer
- Game status packets
- Back-channel metadata
- Remote control commands

**Similar to WebSocket** API with `send()` and `message` events.

### 4. RTCSessionDescription
**SDP (Session Description Protocol)** - Exchange of media capabilities.

Contains:
- Codec preferences (VP8, VP9, H.264, Opus)
- Resolution/quality parameters
- ICE candidates for NAT traversal

---

## Core WebRTC APIs

### getUserMedia() - Capture Media
```javascript
const constraints = {
  video: true,        // or specific resolution
  audio: true
};

navigator.mediaDevices.getUserMedia(constraints)
  .then(stream => {
    localVideo.srcObject = stream;
  })
  .catch(error => {
    console.error('Camera access denied:', error);
  });
```

**Browser permission required** for camera/microphone access.

### RTCPeerConnection - Establish Connection
```javascript
const servers = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "turn:example.com:3478", username: "user", credential: "pass" }
  ]
};

const peerConnection = new RTCPeerConnection(servers);

// Add local stream to connection
peerConnection.addTrack(localStream.getTracks()[0]);

// Listen for ICE candidates (network paths)
peerConnection.addEventListener('icecandidate', (event) => {
  if (event.candidate) {
    // Send to remote peer via signaling channel
    signalingChannel.send({ type: 'candidate', candidate: event.candidate });
  }
});

// Create offer (initiator)
peerConnection.createOffer()
  .then(desc => peerConnection.setLocalDescription(desc))
  .then(() => {
    // Send SDP offer to remote peer via signaling
    signalingChannel.send({ type: 'offer', sdp: peerConnection.localDescription });
  });

// Receive offer, create answer
peerConnection.ontrack = (event) => {
  remoteVideo.srcObject = event.streams[0];
};
```

### RTCDataChannel - Data Exchange
```javascript
// Create data channel
const dataChannel = peerConnection.createDataChannel('chat');

dataChannel.onopen = () => {
  console.log('Data channel opened');
  dataChannel.send('Hello from sender!');
};

dataChannel.onmessage = (event) => {
  console.log('Received:', event.data);
};
```

### Signaling - Connection Setup Exchange
**Critical component:** WebRTC peers need a signaling channel (WebSocket, HTTP, etc.) to exchange:
- ICE candidates (network paths)
- SDP offers/answers (media capabilities)

Example signaling flow:
```
Peer A                                    Peer B
  │                                         │
  ├─ createOffer() ────────────────────────>│
  │  setLocalDescription()                  │
  │  ──────────────────────────────────────>│
  │                                         ├─ setRemoteDescription()
  │                                         ├─ createAnswer()
  │                                         ├─ setLocalDescription()
  │  <──────────────────────────────────────┤
  │  setRemoteDescription()                 │
  │                                         │
  ├─ ICE connection established ───────────────────────
  │    │                                         │
  │    └────── Real-time communication ──────┘
```

---

## ICE, STUN, TURN - NAT Traversal

### The Problem: Firewalls and NAT
- Peers are behind routers/firewalls
- Private IP addresses not routable
- Need to discover public IP and open ports

### Solutions:

#### ICE (Interactive Connectivity Establishment)
**Framework** for finding best path between peers.
- Gathers all possible network interfaces
- Tests connectivity between candidates
- Selects best working path

#### STUN (Session Traversal Utilities for NAT)
**Discovers public IP/port** mapping.
- Server: `stun:stun.l.google.com:19302`
- Returns: "Your public IP is X.X.X.X:PORT"
- Free, public STUN servers available

#### TURN (Traversal Using Relays around NAT)
**Relays traffic** when direct P2P fails (symmetric NAT, strict firewalls).
- Server: `turn:server:port`
- Requires authentication
- Costs money (bandwidth relay)
- Fallback for STUN failures

---

## WebRTC Protocol Stack

```┌─────────────────────────────────────┐
│    Application Layer                │
│   ┌─────────────────────────────┐   │
│   │ RTCDataChannel (SCTP)       │   │
│   │ (for arbitrary data)        │   │
│   └─────────────────────────────┘   │
├─────────────────────────────────────┤
│   Transport Layer                   │
│   ┌─────────────────────────────┐   │
│   │ RTP (Real-time Transport)   │   │
│   │ (for audio/video streams)   │   │
│   └─────────────────────────────┘   │
├─────────────────────────────────────┤
│   Signaling Layer                   │
│   ┌─────────────────────────────┐   │
│   │ SDP (Session Description)   │   │
│   │ (via WebSocket/HTTP)        │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘

ICE/STUN/TURN - Network path discovery
DTLS - Encryption handshake
SRTP - Encrypted media transport
```

---

## WebRTC in EventVikings Predictive Dialer Context

### Integration Architecture

**Hybrid Approach:**
```
┌──────────────────────────────────────────────────┐
│           EventVikings Predictive Dialer         │
├──────────────────────────────────────────────────┤
│  ┌─────────────────┐     ┌─────────────────────┐ │
│  │  SIP Protocol   │     │   WebRTC Browser    │ │
│  │  (FreeSWITCH)   │     │   Agent Interface   │ │
│  └────────┬────────┘     └──────────┬──────────┘ │
│           │                         │             │
│           │         ┌───────────────┘             │
│           │         │                             │
│           ▼         ▼                             │
│  ┌─────────────────────────────────────────────┐ │
│  │         Agent Dashboard (Web Browser)       │ │
│  │  - Call controls (hangup, transfer, hold)   │ │
│  │  - Screen sharing with training             │ │
│  │  - Live monitoring and feedback             │ │
│  │  - DTMF dialing support                     │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### Use Cases for WebRTC:

1. **Agent Desktop**
   - Browser-based call interface
   - No software installation needed
   - Cross-platform compatibility

2. **Screen Sharing**
   - Trainer monitors agent calls in real-time
   - Instant feedback and coaching
   - Compliance recording

3. **Call Recording**
   - Store audio locally or in browser storage
   - Privacy controls (redaction)
   - Export for analytics

4. **DTMF Support**
   - Dial pad integration
   - IVR navigation
   - Customer self-service

5. **Call Transfer**
   - Warm transfer to supervisor
   - Cold transfer to specialized agents
   - Seamless handoff

---

## Browser Compatibility

### Native Support (No adapter needed):
- Chrome 38+
- Firefox 44+
- Safari 11.1+
- Edge 16+

### Legacy Support:
- **adapter.js** - Cross-browser shim library
- **GitHub:** `webrtcHacks/adapter` or `webrtc/adapter`
- Purpose: Normalize browser API differences

---

## Security Considerations

### Required for All Connections:
- **DTLS (Datagram TLS)** - Encryption at transport layer
- **SRTP (Secure RTP)** - Encrypted media streams
- **SCTP over DTLS** - Secure data channels

### Best Practices:
1. **HTTPS Required** - WebRTC only works on secure origins (HTTPS or localhost)
2. **Certificate Authority** - Use valid TLS certificates
3. **User Consent** - Always request camera/mic permissions explicitly
4. **TURN Server Credentials** - Strong authentication, avoid default passwords
5. **Data Encryption** - All WebRTC traffic encrypted by default

---

## Performance Monitoring

### Key Metrics:
```javascript
const stats = await peerConnection.getStats();
stats.forEach(report => {
  // Packet loss, jitter, latency
  // Bytes sent/received
  // Codec information
  // Connection quality
});
```

### Debug Tools:
- **Chrome:** `chrome://webrtc-internals` - Full diagnostic page
- **WebRTC Troubleshooter:** `test.webrtc.org` - Environment checks

---

## Key Takeaways for EventVikings

1. **WebRTC enables browser-based dialer** - No app installation, cross-platform
2. **Signaling server required** - WebSocket or similar for SDP/ICE exchange
3. **TURN server for reliability** - Fallback when direct P2P fails
4. **Works alongside SIP** - Not replacement, complementary technology
5. **Screen sharing capability** - Training, monitoring, compliance
6. **Built-in encryption** - DTLS + SRTP, no additional config needed
7. **adapter.js for compatibility** - Normalize browser differences

---

## Common Pitfalls

1. **Forgetting HTTPS** - WebRTC requires secure context
2. **No signaling server** - Can't establish connections without it
3. **TURN credentials missing** - Fails on strict NATs/firewalls
4. **Browser permission denied** - Must request getUserMedia explicitly
5. **Using old APIs** - Stick to Promise-based APIs, use adapter.js

---

## Next Steps

- **Proficiency:** aware (foundation established)
- **Next level:** basic - implement hands-on with signaling server
- **Prerequisites:** adapter.js integration, WebSocket server setup
- **Mission impact:** HIGH - browser-based agent interface, training tools

---

## References

- **MDN Web Docs** - WebRTC API reference
- **Google Codelabs** - Complete WebRTC implementation guide
- **WebRTC.org** - Official WebRTC project documentation
- **adapter.js** - Cross-browser compatibility library

---

## Status

- **Proficiency:** aware (updated 2026-03-22)
- **Knowledge File:** Created `memory/knowledge/webrtc.md`
- **Context:** Complements SIP Protocol knowledge for EventVikings predictive dialer
- **Next:** Hands-on implementation with signaling server setup
