# Monitoring & Alerts Setup

## Overview
This guide covers the steps to set up real‑time monitoring and alerting for the **MusicGen** and **AudioStudio** production environments using **Sentry** and **PostHog**.

Both services are already configured:
- **Sentry DSN**: `https://bd1230e711170c8e846e3bd2f8f71833@o4510830638202880.ingest.us.sentry.io/4510830640037888`
- **PostHog**: `https://us.posthog.com` (API key stored in `~/.openclaw/workspace/.credentials/posthog.json`)

The goal is to receive instant alerts for:
1. Application errors (exception rate > threshold)
2. API latency spikes
3. Unexpected downtime
4. High CPU / memory usage (via integration with hosting platform)
5. PostHog retention & funnel drop‑off alerts

---

## Sentry Alert Configuration

### 1. Create Error Rate Alert
1. Log in to [Sentry](https://sentry.io/).
2. Navigate to **Projects** → **MusicGen**.
3. Go to **Alerts** → **Create Alert**.
4. Choose **Error rate**.
5. Set threshold: **> 5 errors/min** (adjust based on baseline).
6. Configure notification channels (Slack, email, webhook).
7. Repeat for **AudioStudio**.

### 2. Create Transaction Latency Alert
1. In Sentry, go to **Metrics** → **Transactions**.
2. Select the `request` transaction for your API.
3. Click **Add alert**.
4. Set threshold: **> 2000ms** (2 s) for 2 consecutive minutes.
5. Add notifications.

### 3. Create Availability Alert
1. Go to **Integrations** → **Webhooks**.
2. Add a webhook to Sentry for **Availability**.
3. Set **Down** threshold to **0%**.
4. Add notifications.

---

## PostHog Alert Configuration

### 1. Enable Alerting for Retention
1. In PostHog, open the **Retention** insight you use for MusicGen.
2. Click the **Bell** icon (alert) in the top right.
3. Set trigger: **Retention drop‑off > 20%**.
4. Add Slack or email notification.
5. Repeat for AudioStudio.

### 2. Funnel Drop‑off Alerts
1. Open the funnel insight for the signup → purchase funnel.
2. Set alert on any step with **drop‑off > 30%**.
3. Configure notification.

### 3. Custom Event Alerts
1. Use **Insights** → **New Insight** → **Events**.
2. Create a query for critical events (e.g., `error` events).
3. Set an alert if event count > threshold.

---

## Consolidated Alert Dashboard
Create a simple Slack channel (e.g., `#dev-alerts`) and add both Sentry and PostHog webhooks. Use a bot (e.g., `monitoring-bot`) to aggregate alerts and display a quick status summary daily.

---

## Documentation & Tracking
- Store this guide in `docs/monitoring_setup.md`.
- Create a todo entry `Document monitoring setup` and mark complete once alerts are verified.
- Keep the list of alert thresholds in a `monitoring_thresholds.yaml` for version control.

---

**Next steps:** Verify alerts by triggering a test error in the staging environment and confirm notifications arrive in Slack.
