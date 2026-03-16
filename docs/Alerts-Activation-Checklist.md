# Monitoring Alerts Activation Checklist

**Status:** Ready for manual activation  
**Date:** 2026-03-09  
**Tools:** Sentry (https://sentry.io), PostHog (https://us.posthog.com)

## Pre-flight Check

- [ ] Sentry DSN configured: `https://bd1230e711170c8e846e3bd2f8f71833@o4510830638202880.ingest.us.sentry.io/4510830640037888`
- [ ] PostHog API key available (stored in `~/.openclaw/workspace/.credentials/posthog.json`)
- [ ] Both MusicGen and AudioStudio have Sentry SDK initialized
- [ ] PostHog events being tracked (signup, purchase, feature_use, error)

## Part 1: Sentry Alert Setup

### For MusicGen Project

1. **Log in to Sentry**
   - Navigate to https://sentry.io/
   - Sign in with appropriate credentials
   - Select project: MusicGen

2. **Create Error Rate Alert**
   - Go to **Alerts** → **Create Alert**
   - Alert type: **Error rate**
   - Threshold: **> 5 errors/minute** (adjust based on baseline)
   - Frequency: **Real-time**
   - Notification: Slack channel `#dev-alerts` or email team

3. **Create Latency Alert**
   - Go to **Metrics** → **Transactions**
   - Select `request` transaction
   - Click **Add alert**
   - Threshold: **> 2000ms** (2 seconds)
   - Duration: **2 consecutive minutes**
   - Notification: Same as above

4. **Create Availability Alert**
   - Go to **Integrations** → **Webhooks**
   - Add webhook for **Availability** monitoring
   - Trigger: **0% uptime** (service down)
   - Notification: Same as above

### For AudioStudio Project

Repeat steps 1-4 for AudioStudio project.

### Quick Reference Script

```bash
# Run automated alert setup script
python3 scripts/setup_sentry_alerts.py --project MUSICGEN
python3 scripts/setup_sentry_alerts.py --project AUDIOSTUDIO
```

## Part 2: PostHog Alert Setup

### Retention Drop-off Alert

1. **Open PostHog Dashboard**
   - Navigate to https://us.posthog.com/
   - Select your project

2. **Create/Verify Retention Insight**
   - Go to **Product Analytics** → **Retention**
   - Ensure insight exists for both MusicGen and AudioStudio
   - Filter by product if needed

3. **Set Up Alert**
   - Click **Bell icon** on Retention insight
   - Configure:
     - Trigger: **Retention drop-off > 20% week-over-week**
     - Frequency: **Daily**
     - Channels: Slack `#dev-alerts`, email team

### Funnel Drop-off Alert

1. **Create Funnel Insight**
   - Go to **Product Analytics** → **Funnels**
   - Create funnel: `signup` → `login` → `first_use` → `purchase`
   - Filter by product (MusicGen/AudioStudio)

2. **Set Up Alert**
   - Click **Bell icon** on Funnel insight
   - Configure:
     - Trigger: **Any step drop-off > 30%**
     - Frequency: **Daily**
     - Channels: Same as above

### Error Event Alert

1. **Create Event Alert**
   - Go to **Insights** → **New Insight** → **Events**
   - Query: Event = `error`
   - Set threshold: **> 5 errors/hour**

2. **Set Up Alert**
   - Click **Bell icon**
   - Configure: **Real-time notification**

## Part 3: Notification Channels

### Slack Integration

1. **Connect PostHog to Slack**
   - In PostHog: **Settings** → **Integrations**
   - Click **Slack** → **Connect**
   - Follow OAuth flow
   - Select channel: `#dev-alerts`

2. **Configure Sentry Alerts**
   - In Sentry: **Settings** → **Integrations**
   - Add Slack webhook URL
   - Test notification

### Email Distribution List

Create team email list: `dev-team@zer0daylabs.com`  
Add to both Sentry and PostHog notifications.

## Part 4: Verification

### Test Alerts

1. **Trigger Test Error**
   - Deploy test error to staging
   - Verify alert arrives within 5 minutes

2. **Simulate Latency Spike**
   - Use load testing tool to increase response time
   - Verify latency alert triggers at threshold

3. **Check PostHog Alerts**
   - Trigger test events
   - Verify retention and funnel alerts work

### Verification Checklist

- [ ] Error rate alerts configured for MusicGen
- [ ] Error rate alerts configured for AudioStudio
- [ ] Latency alerts configured for MusicGen
- [ ] Latency alerts configured for AudioStudio
- [ ] Availability alerts configured for both
- [ ] PostHog retention alerts configured
- [ ] PostHog funnel alerts configured
- [ ] PostHog error alerts configured
- [ ] Slack integration active for both platforms
- [ ] Email notifications configured
- [ ] Test alerts successfully triggered and received

## Next Steps After Activation

1. **Monitor alert volume** for first 48 hours
2. **Adjust thresholds** based on actual error rates and latencies
3. **Review false positives** and refine alerts
4. **Schedule weekly alert review** to optimize
5. **Document baseline metrics** for future comparison

---
**Estimated time for full setup:** 30-45 minutes  
**Manual effort:** Dashboard configuration only (no code changes required)
