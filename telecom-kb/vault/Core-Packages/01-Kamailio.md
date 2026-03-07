# Kamailio

## Overview
Kamailio is a powerful open-source SIP proxy server designed for high-performance, scalable SIP applications.

## Purpose
Kamailio serves as the core signaling engine for SIP routing, load balancing, and application logic in telephony systems. It's the backbone of modern SIP-based communications infrastructure.

## Key Concepts

- **Core Function**: SIP proxy, registrar, and application server
- **Role**: Signaling plane orchestrator in the telecom architecture
- **Dependencies**: FreeSWITCH or similar media server, databases for authentication/routing
- **Integration Points**: SIP endpoints, media servers, billing systems, registries

## Architecture

Kamailio operates as a stateful or stateless SIP proxy, processing SIP messages between endpoints and applications.

### Components

- **Core Engine**: Handles SIP message parsing and routing
- **Modules**: Extendable functionality (authentication, routing, recording, etc.)
- **Database Interface**: MySQL, PostgreSQL, Redis for dynamic routing
- **Management Interface**: RPC, XML-RPC for external control

## Configuration

### Essential Settings

```conf
# Basic Kamailio configuration
listen=udp:0.0.0.0:5060
listen=tcp:0.0.0.0:5060
listen=tls:0.0.0.0:5061

# Domain configuration
domain="yourdomain.com"

# Routing logic
route{
    if(is_method("REGISTER")){
        # Handle registrations
        do_register();
    } else {
        # Route calls
        forward();
    }
}
```

### Common Configurations

**Load Balancing**:
```conf
sl_load_balance("fork:127.0.0.1:5070;127.0.0.1:5071")
```

**Authentication**:
```conf
if(is_method("REGISTER")){
    if(!auth("${db_table}","${db_row}")){
        slm_send_status(401,"Unauthorized");
        exit;
    }
    do_register();
}
```

## Usage Patterns

### Typical Workflows

1. SIP REGISTER -> Kamailio authenticates and routes to registrar
2. SIP INVITE -> Kamailio routes to appropriate backend (FreeSWITCH)
3. SIP BYE -> Kamailio handles call termination and logging

### Use Cases

- **SIP Proxy**: Basic SIP signaling routing between endpoints
- **Load Balancer**: Distribute SIP traffic across multiple servers
- **Registrar**: Register SIP endpoints and store location information
- **Application Server**: Implement custom SIP application logic

## Protocols Supported

- SIP (Session Initiation Protocol)
- SDP (Session Description Protocol)
- TLS (Transport Layer Security)
- TCP/UDP/WS/WSS transport

## Integration

This package integrates with:
- [[FreeSWITCH]] - Media processing and conferencing
- [[WebRTC]] - Browser-based SIP clients
- [[Pipecat]] - AI voice integration via SIP
- Database systems (MySQL, PostgreSQL, Redis) for routing tables

## Troubleshooting

### Common Issues

1. **Issue**: Registration failures
   **Solution**: Check database connectivity and auth modules

2. **Issue**: SIP packets not reaching destination
   **Solution**: Verify firewall rules and listen configurations

3. **Issue**: High CPU usage
   **Solution**: Check routing logic complexity and optimize queries

## Best Practices

- Use stateless forwarding for load-balanced deployments
- Implement proper TLS for signaling security
- Configure appropriate timeouts for different transports
- Use Redis for high-speed location lookups
- Monitor packet loss and jitter metrics

## Related Documents

- [[Core-Packages/FreeSWITCH]]
- [[Protocols/SIP]]
- [[Configurations/Kamailio-Setup]]

---
*Created: 2026-03-06*
*Last Updated: 2026-03-06*
