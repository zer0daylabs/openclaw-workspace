# Slack Integration Setup Guide

## Overview
Connect Slack channel `#dev-alerts` to receive automated notifications from Sentry and PostHog.

## Prerequisites
- Slack workspace with admin permissions
- Channel `#dev-alerts` created in workspace
- PostHog and Sentry accounts configured

## Step 1: Create Slack Channel

1. Open Slack workspace
2. Click **Add channels** → **Create a new channel**
3. Name: `dev-alerts`
4. Set to **Public**
5. Add team members who should receive alerts
6. Click **Create channel**

## Step 2: Connect PostHog to Slack

1. Log in to PostHog: https://us.posthog.com
2. Navigate to **Settings** → **Integrations**
3. Click **Slack** → **Connect**
4. Follow OAuth flow:
   - Authorize PostHog to access your Slack workspace
   - Select default channel (keep as `#dev-alerts` or change)
   - Complete authorization
5. Verify connection:
   - PostHog dashboard shows "Slack: Connected"
   - Check `#dev-alerts` for test message

## Step 3: Configure PostHog Alerts

### Alert Types to Configure:

**Retention Alerts:**
1. Open retention insight (Product Analytics → Retention)
2. Click **Bell icon** (top right)
3. Configure:
   - Trigger: Retention drops > 20%
   - Frequency: Daily
   - Channels: `#dev-alerts`

**Funnel Alerts:**
1. Open funnel insight (Product Analytics → Funnels)
2. Click **Bell icon**
3. Configure:
   - Trigger: Any step drop-off > 30%
   - Frequency: Daily
   - Channels: `#dev-alerts`

**Error Event Alerts:**
1. Create events query for `error` events
2. Click **Bell icon**
3. Configure:
   - Trigger: Error count > 5/hour
   - Frequency: Real-time
   - Channels: `#dev-alerts`

## Step 4: Connect Sentry to Slack

1. Log in to Sentry: https://sentry.io
2. Navigate to **Settings** → **Integrations**
3. Click **Slack** → **Connect**
4. Follow OAuth flow:
   - Authorize Sentry to access your Slack workspace
   - Select default channel (`#dev-alerts`)
   - Complete authorization
5. Verify connection:
   - Sentry dashboard shows "Slack: Connected"
   - Check `#dev-alerts` for test message

## Step 5: Configure Sentry Alerts

### Alert Types to Configure:

**MusicGen Project:**
1. Open MusicGen project (sentry.io → Projects → MusicGen)
2. Go to **Alerts** → **Create Alert**
3. **Error Rate Alert:**
   - Threshold: > 5 errors/min
   - Frequency: 15 min
   - Notification: `#dev-alerts`
4. **Latency Alert:**
   - Threshold: > 2000ms
   - Frequency: 15 min
   - Notification: `#dev-alerts`
5. **Availability Alert:**
   - Monitor uptime
   - Trigger: 0% uptime
   - Frequency: 5 min
   - Notification: `#dev-alerts`

**AudioStudio Project:**
- Repeat steps 1-5 for AudioStudio project

## Step 6: Test Alerts

### Test Sentry Alerts:
1. Trigger a test error in staging environment:
   ```python
   raise Exception("Test error - alert verification")
   ```
2. Check `#dev-alerts` for Sentry notification
3. Verify message format and timing

### Test PostHog Alerts:
1. Create a test event in PostHog:
   - Navigate to **Product Analytics** → **Events**
   - Create event: `test_alert_trigger`
2. Check `#dev-alerts` for PostHog notification
3. Verify message format and timing

## Step 7: Verify Configuration

**Checklist:**
- [ ] Slack channel `#dev-alerts` created
- [ ] PostHog Slack integration connected
- [ ] PostHog retention alerts configured
- [ ] PostHog funnel alerts configured
- [ ] PostHog error alerts configured
- [ ] Sentry Slack integration connected
- [ ] Sentry MusicGen alerts configured
- [ ] Sentry AudioStudio alerts configured
- [ ] Test Sentry alert triggers message
- [ ] Test PostHog alert triggers message

## Troubleshooting

**Issue:** Slack integration shows "Disconnected"
- Solution: Re-authorize in PostHog/Sentry settings

**Issue:** No alerts received in Slack
- Solution: Check channel permissions, ensure notifications not muted

**Issue:** Alerts flooding channel
- Solution: Adjust alert thresholds, increase frequency intervals

## Monitoring Slack Activity

**Track alert volume:**
- Use Slack analytics to monitor alert frequency
- Adjust thresholds if too many/few alerts
- Archive old alert messages regularly

**Best Practices:**
- Keep channel dedicated to alerts only
- Use thread replies for alert discussions
- Set up Slack summaries for daily/weekly reports

---
**Estimated Time:** 20 minutes  
**Status:** Ready for execution once databases connected
