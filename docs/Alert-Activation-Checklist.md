# Alert Activation Checklist

## Sentry Alerts

### Pre-conditions
- [ ] Sentry SDK initialized in MusicGen and AudioStudio
- [ ] SENTRY_DSN configured in Vercel environment variables
- [ ] Test events visible in Sentry dashboard

### Alert Rules to Create

#### Error Rate Alert
- [ ] Navigate to Sentry dashboard → Projects → MusicGen → Alerts
- [ ] Create new alert: "MusicGen High Error Rate"
- [ ] Condition: Error count > 5 per minute
- [ ] Frequency: Real-time (5 min)
- [ ] Notification: Slack #dev-alerts, Email

#### Latency Alert
- [ ] Create alert: "MusicGen High Latency"
- [ ] Condition: Transaction p95 > 2000ms for 3 consecutive windows
- [ ] Frequency: 10 minutes
- [ ] Notification: Slack #dev-alerts

#### Availability Alert
- [ ] Create alert: "MusicGen Down"
- [ ] Condition: 0% availability for 2 minutes
- [ ] Frequency: 5 minutes
- [ ] Notification: Email (urgent)

### Repeat for AudioStudio
- [ ] All above alerts created for AudioStudio

## PostHog Alerts

### Retention Alerts
- [ ] Open PostHog → Product Analytics → Retention
- [ ] Create retention insight for MusicGen (7-day, 14-day, 30-day)
- [ ] Set alert: Retention drop > 20% week-over-week
- [ ] Notify: Slack #dev-alerts daily

### Funnel Alerts
- [ ] Open PostHog → Product Analytics → Funnels
- [ ] Create funnel: signup → login → first_use → purchase
- [ ] Set alert: Any step drop-off > 30%
- [ ] Notify: Slack #dev-alerts daily

### Error Event Alert
- [ ] Create events insight for "error" events
- [ ] Set alert: Count > 5 per hour
- [ ] Notify: Slack #dev-alerts real-time

## Final Verification
- [ ] All alerts configured in Sentry and PostHog
- [ ] Test alerts triggered successfully
- [ ] Notifications arriving in Slack #dev-alerts and email
- [ ] Alert thresholds documented in `docs/alert-thresholds.md`
- [ ] Run alert system health check weekly

---
*Created: 2026-03-09 09:05 MST*
