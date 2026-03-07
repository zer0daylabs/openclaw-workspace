# WebRTC

## Overview
WebRTC (Web Real-Time Communication) is a set of protocols and APIs that enable real-time audio, video, and data communication directly between web browsers and applications.

## Purpose
WebRTC provides browser-based real-time media communication without requiring plugins or extensions, enabling direct peer-to-peer media streaming and WebRTC-based telephony clients.

## Key Concepts

- **Core Function**: Real-time media streaming between browsers
- **Role**: Browser-based media client for SIP/WebRTC communication
- **Dependencies**: STUN/TURN servers for NAT traversal, signaling server (WebSocket/SIP)
- **Integration Points**: Kamailio (via WebSIP), FreeSWITCH (mod_sofia), SIP trunks

## Architecture

WebRTC operates as a peer-to-peer media framework with server-assisted connection setup.

### Components

- **RTCDataChannel**: Bidirectional data communication
- **RTCAudioTrack**: Audio capture and playback
- **RTCVideoTrack**: Video capture and playback
- **RTCPeerConnection**: Core connection management
- **STUN/TURN**: NAT traversal infrastructure

## Configuration

### Essential Settings

```javascript
// Basic WebRTC peer connection
const config = {
    iceServers: [
        { urls: "stun:stun.l.google.com:19302" },
        { urls: "turn:your-turn-server:3478", 
          username: "user", 
          credential: "pass" }
    ]
};

const pc = new RTCPeerConnection(config);
```

### Common Configurations

**SIP over WebRTC**:
```javascript
// Using SIP.js for WebRTC SIP client
const userAgent = new SIP.UserAgent({
    uri: "sip:username@domain.com",
    transportOptions: {
        server: "wss://domain.com:5062"
    },
    mediaConstraints: {
        audio: true,
        video: false
    }
});
```

**SDP Offer/Answer**:
```javascript
pc.createOffer().then(offer => {
    pc.setLocalDescription(offer);
    // Send offer to signaling server
}).catch(err => {
    console.error("Offer failed:", err);
});
```

## Usage Patterns

### Typical Workflows

1. Browser initializes RTCPeerConnection
2. STUN/TURN discovery for NAT traversal
3. Signaling exchange via WebSocket
4. ICE candidate gathering and exchange
5. Peer-to-peer media stream establishment

### Use Cases

- **Web Phone**: Browser-based SIP client for softphones
- **Video Conferencing**: Multi-party video calls
- **Screen Sharing**: Share browser tab or desktop
- **Data Channels**: File transfer, chat over WebRTC
- **Call Center**: Agent desktop with embedded browser client

## Protocols Supported

- SIP over WebSocket (WSS)
- DTLS (Data Transfer Layer Security)
- SRTP (Secure Real-time Transport Protocol)
- ICE (Interactive Connectivity Establishment)
- STUN/TURN for NAT traversal

## Integration

This protocol integrates with:
- [[Kamailio]] - SIP routing for WebSIP endpoints
- [[FreeSWITCH]] - mod_sofia WebRTC support
- [[Pipecat]] - AI voice integration for WebRTC clients
- TURN servers for NAT traversal

## Troubleshooting

### Common Issues

1. **Issue**: Connection fails behind NAT
   **Solution**: Configure TURN server and proper ICE candidates

2. **Issue**: Audio/video quality issues
   **Solution**: Check bandwidth, codec compatibility, and network stability

3. **Issue**: Certificate errors
   **Solution**: Ensure proper TLS certificates for signaling server

## Best Practices

- Always use WSS (WebSocket Secure) for signaling
- Configure appropriate TURN servers for enterprise environments
- Use OPUS codec for best audio quality
- Implement ICE restart for connection resilience
- Monitor connection quality metrics (Jitter, packet loss, RTT)

## Related Documents

- [[Core-Packages/Kamailio]]
- [[Core-Packages/FreeSWITCH]]
- [[Core-Packages/Pipecat]]
- [[Protocols/SIP]]

---
*Created: 2026-03-06*
*Last Updated: 2026-03-06*
