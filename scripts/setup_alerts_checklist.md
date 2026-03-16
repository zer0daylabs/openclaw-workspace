# Monitoring Alerts Setup Checklist

## Prerequisites
- [x] Railway cleanup documented: `docs/railway_cleanup.md`
- [x] Auto_vercel_db script ready: `scripts/auto_vercel_db.py`
- [x] Railway-to-Vercel guide: `docs/Railway-to-Vercel-DB-Setup.md`
- [x] Sentry alerts script: `scripts/setup_sentry_alerts.py`
- [x] PostHog alerts guide: `docs/PostHog-Alerts-Setup.md`

## Alert Setup Checklist

### Sentry Alerts
**Project:** MusicGen (edmmusic.studio)
- [ ] 1. Log in to Sentry dashboard (sentry.io)
- [ ] 2. Navigate to MusicGen project
- [ ] 3. Go to **Alerts** → **Create Alert**
- [ ] 4. **Error Rate Alert**: Threshold > 5 errors/min
- [ ] 5. **Latency Alert**: Threshold > 2000ms
- [ ] 6. **Availability Alert**: Monitor uptime
- [ ] 7. Configure notifications (Slack: #dev-alerts)

**Project:** AudioStudio
- [ ] 1. Navigate to AudioStudio project
- [ ] 2. Same alert setup as MusicGen
- [ ] 3. Configure notifications (Slack: #dev-alerts)

### PostHog Alerts
**Retention Analysis**
- [ ] 1. Open PostHog → Product Analytics → Retention
- [ ] 2. Create retention insight for MusicGen
- [ ] 3. Set alert: Retention drops > 20%
- [ ] 4. Repeat for AudioStudio

**Funnel Analysis**
- [ ] 1. Create funnel: signup → login → first_use → purchase
- [ ] 2. Set alert: Any step drop-off > 30%

**Error Events**
- [ ] 1. Create event query for `error` events
- [ ] 2. Set alert: Error count > 5/hour

### Slack Integration
- [ ] 1. Connect PostHog to Slack (Settings → Integrations → Slack)
- [ ] 2. Create channel: #dev-alerts
- [ ] 3. Configure webhook for Sentry alerts

## Testing
- [ ] 1. Trigger test error in staging environment
- [ ] 2. Verify alert arrives in Slack
- [ ] 3. Confirm notification timing and content

## Estimated Time
- Sentry setup: 15-20 minutes
- PostHog setup: 15-20 minutes
- Slack integration: 5 minutes
- **Total:** 35-45 minutes

## Completion Criteria
- All alerts configured in Sentry and PostHog
- Notifications flowing to Slack #dev-alerts
- Test alerts verified and working
- Monitoring active for both products

---
**Status:** Ready for manual UI setup. All scripts and guides created. Execute checklist above to complete.
