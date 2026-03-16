# Infrastructure Verification Checklist

## Purpose
Verify that manual setup steps are complete and all infrastructure components are properly connected and operational.

## Prerequisites
- Manual Railway cleanup completed
- DATABASE_URLs collected and deployed to Vercel
- Monitoring alerts configured in Sentry and PostHog

---

## Phase 1: Railway Cleanup Verification

### Delete Unused DBs
- [ ] Logged into https://railway.app as support@zer0daylabs.com
- [ ] Verified `truthful-warmth` project is deleted
- [ ] Verified `appealing-laughter` project is deleted
- [ ] Railway project count: was 7, should now be 5

### Rename Cryptic Projects
- [ ] Verified `lucky-playfulness` renamed to `MusicGen-DB`
- [ ] Verified `new-db-app` renamed to `AudioStudio-DB`
- [ ] Both projects show updated names in Railway dashboard
- [ ] Both projects still have running Postgres services

**Status:** ☐ Complete | ☐ In Progress | ☐ Not Started

---

## Phase 2: Vercel↔Railway DB Connection Verification

### DATABASE_URL Collection
- [ ] Railway project `MusicGen-DB` has DATABASE_URL visible in Environment Variables
- [ ] Railway project `AudioStudio-DB` has DATABASE_URL visible in Environment Variables
- [ ] Both DATABASE_URLs copied to `docs/railway_db_urls_template.json`
- [ ] Template format verified (postgres://user:pass@host:port/db?sslmode=require)

### Vercel Environment Variable Deployment
- [ ] Executed: `python3 scripts/auto_vercel_db.py --config docs/railway_db_urls_template.json`
- [ ] Vercel project `edmmusic.studio` has DATABASE_URL set in Environment Variables
- [ ] Vercel project `AudioStudio` (audiostudio.ai) has DATABASE_URL set
- [ ] Both deployments triggered automatically
- [ ] Deployments completed successfully (checked Vercel dashboard)

### Database Connection Verification
- [ ] MusicGen (edmmusic.studio) loads without database errors
- [ ] AudioStudio (audiostudio.ai) loads without database errors
- [ ] Railway DB services running (check Railway dashboard)
- [ ] Test loop generation in MusicGen works end-to-end
- [ ] No connection errors in Vercel logs

**Status:** ☐ Complete | ☐ In Progress | ☐ Not Started

---

## Phase 3: Monitoring Alerts Verification

### Sentry Alerts
- [ ] Logged into Sentry dashboard (sentry.io)
- [ ] MusicGen project has error rate alert configured (threshold > 5 errors/min)
- [ ] MusicGen project has latency alert configured (threshold > 2000ms)
- [ ] AudioStudio project has error rate alert configured
- [ ] AudioStudio project has latency alert configured
- [ ] Slack #dev-alerts webhook configured for Sentry notifications
- [ ] Test error triggers notification (verified)

**Status:** ☐ Complete | ☐ In Progress | ☐ Not Started

### PostHog Alerts
- [ ] Logged into PostHog (https://us.posthog.com)
- [ ] MusicGen retention insight created with alert (> 20% dropoff)
- [ ] AudioStudio retention insight created with alert
- [ ] Funnel analysis insight created with alert (> 30% dropoff)
- [ ] Error event query created with alert (> 5 errors/hour)
- [ ] PostHog Slack integration configured
- [ ] Slack #dev-alerts connected for PostHog notifications
- [ ] Test alert triggers notification (verified)

**Status:** ☐ Complete | ☐ In Progress | ☐ Not Started

---

## Phase 4: Overall System Health

### Product Health
- [ ] MusicGen (edmmusic.studio) - production live, responding correctly
- [ ] AudioStudio (audiostudio.ai) - production live, responding correctly
- [ ] Both products show no critical errors in Sentry
- [ ] Both products showing user activity in PostHog

### Cost Monitoring
- [ ] Cost monitoring script operational: `scripts/cost_monitor.py`
- [ ] Railway balance logged (check logs/cost_monitor.log)
- [ ] MRR stable at $9.99
- [ ] Infrastructure costs tracked

### Infrastructure Health Score
- Authentication verified: ✅
- Products healthy: ✅
- Railway cleanup: [ ] Complete | [ ] Pending
- Vercel↔Railway DB: [ ] Complete | [ ] Pending
- Monitoring alerts: [ ] Complete | [ ] Pending

**Final Score:** ☐ 9/10 | ☐ 8/10 | ☐ 7/10 | ☐ < 7/10

---

## Sign-off

**Completed by:** ________________  
**Date:** ________________  
**Time:** ________________  

**Notes:**

---

**This checklist should be completed sequentially. Each phase must be verified before proceeding to the next.**
