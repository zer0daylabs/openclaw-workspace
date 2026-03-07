# GOG CLI Setup - Zer0Day Labs

## Status: ✅ Configured and Tested

### Account Configuration
- **Email:** didvip@gmail.com (default account)
- **Auth Status:** OAuth authenticated
- **Token Created:** 2026-03-06T06:56:20Z (fresh)
- **Scopes:** gmail,calendar,chat,classroom,drive,docs,slides,contacts,tasks,sheets,people,forms,appscript

### Gmail Access ✅
- Connection verified
- Recent activity: Multiple unread emails detected
- Can search, read, send, organize emails

### Calendar Access ✅
- Primary calendar: didvip@gmail.com (owner access)
- US Holidays calendar: read-only
- Email notifications enabled for: event creation, changes, cancellations, RSVPs
- Timezone: America/Phoenix (MST)

### Usage for Heartbeat Monitoring

**Check Recent Emails (Inbox):**
```bash
gog gmail search -a didvip@gmail.com "in:inbox" -j --limit 10
```

**Check Unread Emails:**
```bash
gog gmail search -a didvip@gmail.com "is:unread" -j --limit 5
```

**Check Calendar Events (Next 24h):**
```bash
gog calendar events didvip@gmail@gmail.com --limit 10 --json
```

**Check Today's Schedule:**
```bash
gog calendar search -a didvip@gmail.com "today" -j
```

### Quick Commands Reference

| Task | Command |
|------|---------|
| Search Gmail | `gog gmail search <query> --json` |
| List calendar events | `gog calendar events <calendar> --json` |
| Send email | `gog gmail send` |
| Check auth | `gog auth list` |
| Version | `gog --version` |

### For Cron/Heartbeat Integration
Store commands in a script and call them from heartbeat cron jobs. Example heartbeat check:
- Every 30min: Check for urgent emails (`is:unread label:urgent`)
- Every hour: Check calendar for next 24h events
- Daily morning: Full inbox review

## Notes
- Primary account configured via `gog auth set-account --default didvip@gmail.com`
- All API calls authenticated via OAuth token bucket
- Token auto-refreshes as needed
