# PostHog Alert Setup Guide

## Overview
This guide covers setting up alerts in PostHog for MusicGen and AudioStudio.

## Prerequisites
- PostHog account configured
- Events being tracked (signup, purchase, feature_use, etc.)

## Step 1: Create PostHog Insights

### Retention Analysis
1. Navigate to **Product Analytics** → **Retention**
2. Select your product (MusicGen or AudioStudio)
3. Configure retention period (7, 14, 30 days)
4. Save the insight

### Funnel Analysis
1. Navigate to **Product Analytics** → **Funnels**
2. Create funnel: `signup` → `login` → `first_use` → `purchase`
3. Configure step properties as needed
4. Save the insight

## Step 2: Set Up Alerts

### Retention Drop-off Alert
1. Open the Retention insight
2. Click the **Bell icon** (top right)
3. Configure alert:
   - Trigger: Retention drops > 20% week-over-week
   - Frequency: Daily
   - Channels: Slack, Email

### Funnel Drop-off Alert
1. Open the Funnel insight
2. Click the **Bell icon**
3. Configure alert:
   - Trigger: Any step drop-off > 30%
   - Frequency: Daily
   - Channels: Slack, Email

### Error Event Alert
1. Create a new Insight → **Events**
2. Query for `error` events
3. Set up alert:
   - Trigger: Error count > 5 per hour
   - Frequency: Real-time
   - Channels: Slack, Email

## Step 3: Notification Channels

### Slack Integration
1. In PostHog, go to **Settings** → **Integrations**
2. Click **Slack** → **Connect**
3. Follow OAuth flow to authorize
4. Create channel `#dev-alerts` for centralized alerts

### Email Notifications
1. Add team member emails to PostHog notifications
2. Set up distribution list (e.g., `dev-team@zer0daylabs.com`)

## Step 4: Test Alerts
1. Trigger a test event (e.g., simulate error)
2. Verify alert arrives in Slack/email
3. Adjust thresholds as needed

## Monitoring Checklist
- [ ] Retention alert created for MusicGen
- [ ] Retention alert created for AudioStudio
- [ ] Funnel alert created for MusicGen
- [ ] Funnel alert created for AudioStudio
- [ ] Error alert created for MusicGen
- [ ] Error alert created for AudioStudio
- [ ] Slack integration configured
- [ ] Email notifications configured
- [ ] Alerts tested and verified

---
**Estimated time:** 30 minutes for full setup
**Manual effort required:** PostHog UI configuration
