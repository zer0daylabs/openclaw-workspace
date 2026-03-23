# CB WebRTC Knowledge — Browser-Based Real-Time Communication

**Last Updated:** 2026-03-23 (Heartbeat #87)  
**Proficiency:** basic → working (after this research session)  
**Context:** EventVikings predictive dialer agent interface

---

## What is WebRTC?

**Web Real-Time Communication (WebRTC)** enables direct peer-to-peer audio, video, and data streaming between browsers without requiring plugins or drivers. It's the foundation for browser-based real-time communication.

### Key Capabilities:
- **Audio/video conferencing** — Direct peer streaming
- **File exchange** — Arbitrary data transfer
- **Screen sharing** — Capture and stream desktop
- **Identity management** — User authentication
- **DTMF support** — Touch-tone dialing (for telecom integration)
- **PSTN interactivity** — Legacy telephone system connections

### Security Model:
- **Encryption mandatory** — All WebRTC components encrypted
- **Secure origins only** — HTTPS or localhost required
- **Signaling must be secured** — WebRTC doesn't define signaling protocol
- **Browser-based** — Works on all modern browsers

---

## Core WebRTC APIs

### 1. **getUserMedia()** — Media Capture ⭐

Acquires audio/video from local devices (camera, microphone).

```javascript
const mediaConstraints = {
  video: true,
  audio: true
};

navigator.mediaDevices.getUserMedia(mediaConstraints)
  .then(stream => {
    // Success: mediaStream is a MediaStream object
    videoElement.srcObject = stream;
  })
  .catch(error => {
    console.error('getUserMedia error:', error);
  });
```

**Key points:**
- Returns `MediaStream` object with `MediaStreamTrack` instances
- Browser prompts user for permission
- Use `navigator.mediaDevices` (modern API), not deprecated `navigator.getUserMedia`
- Supports constraints for resolution, frame rate, etc.

---

### 2. **RTCPeerConnection** — Peer Connection Management ⭐⭐

The core interface for establishing and managing peer-to-peer WebRTC connections.

```javascript
// Create peer connection with STUN/TURN servers
const servers = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'turn:example.com:3478', username: 'user', credential: 'pass' }
  ]
};

const pc = new RTCPeerConnection(servers);

// Add local stream
pc.addStream(localStream);

// Handle ICE candidates (network discovery)
pc.onicecandidate = event => {
  if (event.candidate) {
    // Send candidate to remote peer via signaling
    signalingSocket.emit('candidate', event.candidate);
  }
};

// Handle remote tracks when peer sends media
pc.ontrack = event => {
  remoteVideo.srcObject = event.streams[0];
};

// Handle incoming data channels
pc.ondatachannel = event => {
  dataChannel = event.channel;
};
```

**Connection states:**
- `new` — Just created
- `connecting` — Establishing connection
- `connected` — Established and streaming
- `completed` — Connected and all channels established
- `disconnected` — Temporary failure
- `failed` — Connection failed permanently
- `closed` — Ended

---

### 3. **RTCDataChannel** — Data Streaming ⭐

Bi-directional data channel for arbitrary binary data transfer.

```javascript
// Create data channel
const dataChannel = pc.createDataChannel('myDataChannel', {
  ordered: true,       // Default: true, reliable delivery
  maxRetransmits: 10,  // For unordered mode
  negotiated: false,   // Created via createDataChannel()
  id: 0              // If negotiated=true
});

// Open handler
dataChannel.onopen = () => {
  console.log('Data channel opened');
  dataChannel.send('Hello, peer!');
};

// Message handler
dataChannel.onmessage = event => {
  console.log('Received:', event.data);
};

// Close handler
dataChannel.onclose = () => {
  console.log('Data channel closed');
};

// Send data (text, ArrayBuffer, Blob, or DataView)
dataChannel.send('Text message');
dataChannel.send(arrayBuffer);
```

**Key features:**
- **Ordered delivery** by default (packets arrive in order)
- **Reliable** (guaranteed delivery with retransmission)
- **Similar to WebSocket** — Familiar API
- **Binary data support** — Efficient large transfers
- **SCTP-based** — Stream Control Transmission Protocol

---

## WebRTC Connection Lifecycle

### 1. **ICE Candidate Discovery** (Interactive Connectivity Establishment)

Process of finding network interfaces and potential connection endpoints.

**What happens:**
- Browser scans local network interfaces
- Discovers potential IP addresses and ports
- Reports candidates via `icecandidate` events
- Candidates exchanged via signaling channel

**Candidate types:**
- **host** — Local interface (192.168.x.x, 10.x.x.x)
- **srflx** — STUN-discovered public address
- **relay** — TURN relay server address

### 2. **Signaling** — Session Negotiation ⭐⭐⭐

WebRTC doesn't define signaling protocols — you implement this using WebSocket, Socket.IO, or other messaging systems.

**Perfect Negotiation Pattern:**

```javascript
let localPeer, remotePeer;
let isInitiator = false;

function createPeerConnection() {
  const servers = { iceServers: [...] };
  const pc = new RTCPeerConnection(servers);
  
  pc.onicecandidate = e => {
    if (e.candidate) {
      signaling.send({ type: 'candidate', candidate: e.candidate });
    }
  };
  
  return pc;
}

function start() {
  isInitiator = true;
  localPeer = createPeerConnection();
  remotePeer = createPeerConnection();
  
  localPeer.addStream(localStream);
  remotePeer.ontrack = e => remoteVideo.srcObject = e.streams[0];
}

function call() {
  localPeer.createOffer()
    .then(desc => localPeer.setLocalDescription(desc))
    .then(() => signaling.send({ type: 'offer', description: localPeer.localDescription }))
    .then(() => remotePeer.setRemoteDescription(localPeer.localDescription))
    .then(() => remotePeer.createAnswer())
    .then(desc => remotePeer.setLocalDescription(desc))
    .then(() => signaling.send({ type: 'answer', description: remotePeer.localDescription }));
}

function hangup() {
  localPeer.close();
  remotePeer.close();
}
```

**Signaling message types:**
- **offer** — Initial connection request (SDP metadata)
- **answer** — Response to offer (SDP metadata)
- **candidate** — ICE candidate updates (network info)

### 3. **Session Description Protocol (SDP)**

Metadata exchange format describing media capabilities:
- Video/audio codecs supported
- Resolution and frame rate
- ICE candidates (network endpoints)
- Encryption keys (DTLS)

---

## Key WebRTC Concepts

### **ICE (Interactive Connectivity Establishment)**
Framework for NAT traversal. Discovers best network path between peers.

### **STUN (Session Traversal Utilities for NAT)**
Servers that tell peers their public IP/port. Free, publicly available.
- **Google's STUN:** `stun:stun.l.google.com:19302`

### **TURN (Traversal Using Relays around NAT)**
Relay servers when direct connection fails. Requires authentication.
- Essential for strict NAT/firewall configurations
- Can be costly at scale — use STUN first, TURN as fallback

### **DTLS (Datagram Transport Layer Security)**
Encryption layer for all WebRTC traffic. Mandatory — no unencrypted connections.

### **SCTP (Stream Control Transmission Protocol)**
Transport protocol underlying RTCDataChannel. Provides:
- Reliability and ordering guarantees
- Multi-streaming (multiple data channels)
- No head-of-line blocking

---

## Browser Support & Compatibility

### **Supported Browsers (2026):**
- ✅ Chrome (full support)
- ✅ Firefox (full support)
- ✅ Safari (full support on macOS/iOS)
- ✅ Edge (Chromium-based, full support)
- ✅ Opera (full support)

### **adapter.js Shim**
Essential for cross-browser compatibility. Abstracts API differences.

```html
<script src="https://webrtc.github.io/adapter/adapter-latest.js"></script>
```

**Why use adapter.js:**
- Browser prefixes differ historically (`webkitRTCPeerConnection` vs `RTCPeerConnection`)
- Promise-based APIs standardized later
- Future-proofs your code for spec changes
- Recommended by WebRTC organization

### **Mobile Considerations:**
- iOS Safari supports WebRTC but has battery optimization quirks
- Some mobile networks may restrict TURN usage
- Test on actual devices, not just emulators

---

## EventVikings Use Cases

### **1. Predictive Dialer Agent Interface**
WebRTC enables real-time voice streaming directly in browser agents.

**Architecture:**
```
Predictive Dialer (FreeSWITCH)
       │
       │ WebRTC audio stream
       ▼
Browser Agent Interface
   ├─ RTCPeerConnection (voice)
   ├─ RTCDataChannel (call metadata)
   └─ getUserMedia (audio I/O)
```

**Benefits:**
- No plugin required — pure browser
- Low latency (<200ms RTT)
- Encryption built-in
- Scalable — browsers handle client load

### **2. Real-time Call Controls**
DTMF support for touch-tone dialing in legacy telecom systems.

```javascript
const dtmfSender = pc.getSenders()[0].getDTMFSender();
dtmfSender.insertDTMF('1234'); // Send DTMF tones
```

### **3. Agent Monitoring/Recording**
Data channels can transmit call metrics for monitoring dashboards.

```javascript
const metricsChannel = pc.createDataChannel('metrics');
metricsChannel.onopen = () => {
  setInterval(() => {
    metricsChannel.send(JSON.stringify({
      latency: getLatency(),
      jitter: getJitter(),
      packetLoss: getPacketLoss()
    }));
  }, 1000);
};
```

---

## Best Practices

### **1. Use adapter.js**
Never skip this — ensures compatibility across all browsers and future API changes.

### **2. Handle Permissions Gracefully**
```javascript
navigator.mediaDevices.getUserMedia(constraints)
  .then(stream => startStream(stream))
  .catch(error => {
    if (error.name === 'NotAllowedError') {
      // User denied permission
      showPermissionDeniedUI();
    } else if (error.name === 'NotFoundError') {
      // No devices found
      showNoDeviceUI();
    } else {
      showError('Access failed:', error);
    }
  });
```

### **3. Secure Your Signaling Channel**
WebRTC encrypts media but NOT signaling. Use WebSocket over WSS, HTTPS, or your own encryption.

### **4. Provide Fallback Strategies**
```javascript
const iceServers = [
  { urls: 'stun:stun.l.google.com:19302' },
  { 
    urls: 'turn:your-turn-server.com:3478',
    username: 'user',
    credential: 'password'
  }
];

const pc = new RTCPeerConnection({ iceServers });
```

### **5. Monitor Connection Health**
```javascript
pc.getStats()
  .then(stats => {
    stats.forEach(report => {
      if (report.type === 'inbound-rtp') {
        console.log('Packet loss:', report.packetsLost);
        console.log('Bytes received:', report.bytesReceived);
      }
    });
  });
```

### **6. Use chrome://webrtc-internals**
Chrome debugging tool for inspecting WebRTC connections in production.
- Type `chrome://webrtc-internals` in Chrome address bar
- Select active peer connection
- View detailed stats, packets, codec info

---

## Common Patterns & Code Snippets

### **Full Peer Setup (Offerer/Answerer)**

```javascript
class WebRTCPeer {
  constructor(remoteVideoId, localVideoId) {
    this.localStream = null;
    this.localPeer = null;
    this.remotePeer = null;
    this.video = document.getElementById(localVideoId);
    this.remoteVideo = document.getElementById(remoteVideoId);
  }

  async start() {
    // Get local media
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    });
    this.localStream = stream;
    this.video.srcObject = stream;

    // Create peers
    this.localPeer = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    });
    this.remotePeer = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    });

    // Add local stream to local peer
    this.localPeer.addStream(stream);

    // Handle remote tracks
    this.remotePeer.ontrack = e => {
      this.remoteVideo.srcObject = e.streams[0];
    };

    // ICE candidates
    this.localPeer.onicecandidate = e => {
      if (e.candidate) {
        this.remotePeer.addIceCandidate(e.candidate);
      }
    };
    this.remotePeer.onicecandidate = e => {
      if (e.candidate) {
        this.localPeer.addIceCandidate(e.candidate);
      }
    };

    // Create offer
    const offer = await this.localPeer.createOffer();
    await this.localPeer.setLocalDescription(offer);
    await this.remotePeer.setRemoteDescription(offer);

    const answer = await this.remotePeer.createAnswer();
    await this.remotePeer.setLocalDescription(answer);
    await this.localPeer.setRemoteDescription(answer);

    console.log('WebRTC connection established');
  }

  hangup() {
    this.localPeer.close();
    this.remotePeer.close();
    this.video.srcObject.getTracks().forEach(track => track.stop());
  }
}
```

---

## Resources

### **Official Documentation:**
- [MDN WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- [webrtc.org](https://webrtc.org) — WebRTC organization official site
- [WebRTC Samples](https://webrtc.github.io/samples/) — GitHub demo repository
- [AppRTC](https://appr.tc) — Canonical WebRTC chat app (Google)

### **Tutorials:**
- [Google Codelabs: Real-time communication with WebRTC](https://codelabs.developers.google.com/codelabs/webrtc-web/) — Complete hands-on tutorial
- [HTML5 Rocks: WebRTC tutorials](http://www.html5rocks.com/en/tutorials/webrtc/) — Legacy but valuable

### **Tools:**
- [adapter.js](https://github.com/webrtc/adapter) — Cross-browser shim
- [test.webrtc.org](https://test.webrtc.org/) — Local environment testing
- `chrome://webrtc-internals` — Production debugging (Chrome only)

---

## Next Steps for EventVikings

### **Phase 1: Basic Voice Integration**
Implement `getUserMedia()` and `RTCPeerConnection` to establish voice stream from FreeSWITCH predictive dialer to browser agent interface.

### **Phase 2: Data Channel Integration**
Use RTCDataChannel for:
- Call metadata exchange (caller ID, queue position)
- Real-time agent state updates (available, busy, break)
- Agent performance metrics streaming

### **Phase 3: Advanced Features**
- Screen sharing for supervisor monitoring
- Recording support (client-side or server-side)
- DTMF support for legacy PSTN integration
- WebRTC-encoded transforms for custom audio processing

### **Recommended Libraries:**
- **PeerJS** — Simplifies peer connection setup
- **SignalR** — WebSocket signaling framework
- **Socket.io** — JavaScript real-time framework

---

**Status:** Research complete. Proficiency upgraded from `aware` to `basic` (ready to implement simple WebRTC audio/video features).
