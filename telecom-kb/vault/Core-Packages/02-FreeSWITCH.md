# FreeSWITCH

## Overview
FreeSWITCH is a scalable open-source telephony platform that provides media processing, call control, and conferencing capabilities.

## Purpose
FreeSWITCH serves as the media server and call control engine in telecom systems, handling audio/video streams, conferencing, recording, and complex call flows.

## Key Concepts

- **Core Function**: Media processing and call control
- **Role**: Media plane orchestrator, handling RTP streams and call logic
- **Dependencies**: Kamailio for signaling, libraries (speex, gsm, opus), database for configurations
- **Integration Points**: SIP trunks, GSM gateways, WebRTC clients, AI voice services

## Architecture

FreeSWITCH operates as a modular media server with Lua, Python, and Java scripting capabilities.

### Components

- **Core Engine**: Session management and media processing
- **Modules**: Extensible functionality (codecs, protocols, applications)
- **Event Socket**: External control interface for applications
- **Ari Interface**: Async API for modern integrations
- **XML Interface**: XML-based call flows and IVR

## Configuration

### Essential Settings

```conf
# Directory structure
directories.conf:
  <include file="conf/directories.xml" />

# SIP profiles
sofia.conf:
  <profiles>
    <name>internal</name>
    <params>
      <param name="listen-ip" value="0.0.0.0"/>
      <param name="listen-port" value="5061"/>
    </params>
  </profiles>

# Call flows
confxml.conf:
  <document type="freeswitch/xml">
    <include file="DIALPLAN_DIRECTORY/*"/>
  </document>
```

### Common Configurations

**SIP Trunk Configuration**:
```xml
<!-- sofia.conf -->
<profile name="trunk">
  <param name="ext-rtp-ip" value="AUTO_NAT"/>
  <param name="ext-sip-ip" value="YOUR_PUBLIC_IP"/>
  <param name="inbound-codec-prefs" value="PCMU,PCMA"/>
  <param name="outbound-codec-prefs" value="PCMU,PCMA,G722"/>
</profile>
```

**IVR Flow**:
```xml
<!-- Dialplan -->
<extension name="ivr_menu">
  <condition field="destination_number" expression="^100$">
    <action application="answer"/>
    <action application="play_sound" string="ivr/ivr-welcome.wav"/>
    <action application="play_sound" string="ivr/ivr-press-one-to-sales.wav"/>
    <action application="bridge" string="user/101"/>
  </condition>
</extension>
```

## Usage Patterns

### Typical Workflows

1. SIP INVITE from Kamailio -> FreeSWITCH answers and routes call
2. Media stream negotiation -> RTP session established
3. Call processing -> IVR, conferencing, or recording
4. Call termination -> BYE message and billing record

### Use Cases

- **Media Server**: RTP/RTCP stream handling, transcoding
- **Conferencing**: Multi-party audio/video conferences
- **Recording**: Call recording with various formats
- **IVR**: Interactive voice response systems
- **VoIP PBX**: Complete telephony system with extensions

## Protocols Supported

- SIP (Session Initiation Protocol)
- RTP/RTCP (Real-time Transport Protocol)
- H.323 (via module)
- WebRTC (via mod_sofia WebSocket)
- IAX2 (Inter-Asterisk eXchange)

## Integration

This package integrates with:
- [[Kamailio]] - SIP signaling and routing
- [[WebRTC]] - Browser-based clients via WebSocket
- [[Pipecat]] - AI voice processing integration
- STK (Freeswitch ToolKit) for external control

## Troubleshooting

### Common Issues

1. **Issue**: One-way audio
   **Solution**: Check NAT settings and RTP IP configuration

2. **Issue**: Call drops
   **Solution**: Verify timeout settings and network stability

3. **Issue**: Codec negotiation failures
   **Solution**: Ensure codec compatibility between endpoints

## Best Practices

- Use OPUS codec for best quality/efficiency
- Implement proper NAT traversal with STUN/TURN
- Configure appropriate DTMF detection modes
- Monitor media streams for quality issues
- Use external databases for call routing

## Related Documents

- [[Core-Packages/Kamailio]]
- [[Protocols/SIP]]
- [[Features/Conferencing]]

---
*Created: 2026-03-06*
*Last Updated: 2026-03-06*
