# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Communication

- **Primary channel:** Slack (preferred)

## Password Vault Manager 🔐

**Two options installed on clawhub:**

### 1. Local Passwords Vault (recommended for security)
- Skill name: `passwords`
- Storage: `~/.vault/` (encrypted locally with `age`)
- Encryption: Argon2id key derivation + ChaCha20-Poly1305
- No cloud dependency - everything stays local
- Sensitivity levels: low/medium/high/critical
- TOTP/2FA code support
- Audit logs and pattern detection
- **Best for:** API keys, Stripe keys, AI provider secrets

### 2. Bitwarden (for cloud sync)
- Skill name: `bitwarden`
- Self-hostable or cloud (bitwarden.com)
- Cross-device sync
- **Best for:** Shared passwords, cross-device access

**Recommendation:**
- **Use local passwords vault** for sensitive API keys (Stripe, AI providers, etc.)
- **Bitwarden** if you need cross-device access or sharing
- Both skills are installed and ready

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
