# Manual Action Readiness Checklist ⚡

**Purpose:** Quick reference for all manual dashboard actions required to complete infrastructure setup.

**Total Time:** ~70 minutes one-time effort

---

## Step 1: Railway Dashboard Cleanup (10-15 minutes)

**Action:** Login to Railway dashboard and perform cleanup

**URL:** https://railway.app
**Account:** support@zer0daylabs.com

### Tasks:
1. ✅ Navigate to **Projects** → **zer0day** workspace
2. ✅ **Delete** `truthful-warmth` (ID: `4b9635d2-aed0-4464-b6f5-b1386123ddd9`)
   - Click project → Settings → Danger Zone → Delete Project
3. ✅ **Delete** `appealing-laughter` (ID: `3cafd6b5-75b8-4fa7-9ade-abe946180450`)
   - Click project → Settings → Danger Zone → Delete Project
4. ✅ **Rename** `lucky-playfulness` → `MusicGen-DB`
   - Click project → Settings → Rename Project → Enter "MusicGen-DB" → Save
5. ✅ **Rename** `new-db-app` → `AudioStudio-DB`
   - Click project → Settings → Rename Project → Enter "AudioStudio-DB" → Save
6. ✅ **Copy DATABASE_URL** from `MusicGen-DB` (Environment Variables)
7. ✅ **Copy DATABASE_URL** from `AudioStudio-DB` (Environment Variables)

**Documentation:** `docs/railway_cleanup.md`

---

## Step 2: Deploy DATABASE_URLs (5-10 minutes)

**Action:** Populate template and run automation script

### Tasks:
1. ✅ Open `docs/railway_db_urls_template.json`
2. ✅ Replace placeholders with actual DATABASE_URLs:
   ```json
   {
     "MusicGen": "postgres://actual-user:actual-password@actual-host:5432/actual-db?sslmode=require",
     "AudioStudio": "postgres://actual-user:actual-password@actual-host:5432/actual-db?sslmode=require"
   }
   ```
3. ✅ Open terminal and execute:
   ```bash
   cd ~/.openclaw/workspace
   python3 scripts/auto_vercel_db.py --config docs/railway_db_urls_template.json
   ```
4. ✅ Verify both Vercel deployments complete successfully (check Vercel dashboard)
5. ✅ Confirm no database connection errors in application logs

**Documentation:** `docs/Railway-to-Vercel-DB-Setup.md`

---

## Step 3: Activate Monitoring Alerts (35-45 minutes)

**Action:** Configure alerts in Sentry and PostHog dashboards

### Sentry Alerts (~20 min):
1. ✅ Log in to https://sentry.io
2. ✅ Navigate to **MusicGen** project
3. ✅ Create **Error Rate Alert**: Threshold > 5 errors/min
4. ✅ Create **Latency Alert**: Threshold > 2000ms
5. ✅ Create **Availability Alert**: Monitor uptime 100%
6. ✅ Configure Slack webhook → channel: `#dev-alerts`
7. ✅ Repeat steps 2-6 for **AudioStudio** project

### PostHog Alerts (~15 min):
1. ✅ Log in to https://us.posthog.com
2. ✅ Create **Retention Insight** for MusicGen
   - Set alert: Retention drops > 20%
3. ✅ Create **Retention Insight** for AudioStudio
   - Set alert: Retention drops > 20%
4. ✅ Create **Funnel Insight**: signup → login → first_use → purchase
   - Set alert: Any step drop-off > 30%
5. ✅ Create **Error Event Alert**: > 5 errors/hour
6. ✅ Connect PostHog to Slack (Settings → Integrations → Slack)
7. ✅ Verify notifications flow to `#dev-alerts`

**Documentation:** `scripts/setup_alerts_checklist.md`, `docs/PostHog-Alerts-Setup.md`

---

## Step 4: Verify Completion (~5 min)

**Action:** Confirm all manual steps completed successfully

### Tasks:
1. ✅ Railway projects list shows 5 projects (was 7, deleted 2)
2. ✅ Project names updated to MusicGen-DB and AudioStudio-DB
3. ✅ Vercel projects show new DATABASE_URL environment variables
4. ✅ Both applications loading without database errors
5. ✅ Test error triggers Slack notification
6. ✅ Run verification checklist: `docs/infrastructure_verification.md`

---

## Quick Links

| Document | Purpose |
|----------|---------|
| `docs/railway_cleanup.md` | Step-by-step Railway cleanup instructions |
| `docs/railway_db_urls_template.json` | Template for DATABASE_URLs |
| `docs/Railway-to-Vercel-DB-Setup.md` | Complete DB setup guide |
| `scripts/setup_alerts_checklist.md` | Alert setup checklist |
| `docs/PostHog-Alerts-Setup.md` | PostHog alert configuration |
| `docs/infrastructure_verification.md` | Final verification checklist |
| `scripts/auto_vercel_db.py` | Automation script |

---

## Sign-off

**Completed by:** ________  
**Date:** ________  
**Time:** ________  

**Infrastructure Health After Setup:** ☐ 8/10 | ☐ 9/10 | ☐ 10/10
