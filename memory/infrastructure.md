# Infrastructure — Durable Reference

## Hosting & Deployment
- **Vercel:** Team "zer0day" — hosts MusicGen and AudioStudio
- **Railway:** Ready, no active projects yet
- **Domain registrar:** (check when needed)

## Communication
- **Primary:** Slack (#cb channel, ID: C0AD1M21ZV0)
- **Backup:** Webchat (localhost:18789)
- **Slash command:** /openclaw enabled in Slack

## Email
- **Business:** O365 (support@zer0daylabs.com)
- **Transactional:** Resend
  - notifications.edmmusic.studio
  - notifications.audiostudio.ai

## Monitoring
- **Errors:** Sentry
- **Analytics:** Posthog

## OpenClaw Gateway
- **Host:** zer0day (Linux)
- **Version:** 2026.3.2
- **Port:** 18789 (loopback)
- **Primary model:** ollama/qwen3.5:35b (on 192.168.0.143:11434)
- **Fallback model:** ollama/gpt-oss:20b
- **Memory search:** Ollama nomic-embed-text embeddings
- **Heartbeat:** 1h interval, active 08:00-23:00 MST
- **Systemd service:** openclaw-gateway (user service)
- **Logs:** /tmp/openclaw/openclaw-YYYY-MM-DD.log
- **Config:** ~/.openclaw/openclaw.json

## AI / LLM Infrastructure
- **Ollama server:** 192.168.0.143:11434
- **Models available:** qwen3.5:35b, gpt-oss:20b, deepseek-r1:14b, llama3.1:8b, qwen2.5-coder:14b
- **Cloud providers configured:** Anthropic (API key), OpenAI (API key)
- **Embedding model:** nomic-embed-text (via Ollama)

## Credentials Location
- **Stripe:** ~/.openclaw/workspace/.credentials/stripe.json
- **OpenClaw auth profiles:** ~/.openclaw/agents/main/agent/auth-profiles.json
- **Slack tokens:** In openclaw.json (channels.slack)
