# Quick Start: Auto Connect Railway DBs to Vercel

## Prerequisites
- ✅ Railway manual cleanup completed (verified via `scripts/verify_railway_cleanup.py`)
- ✅ DATABASE_URLs collected from Railway projects
- ✅ Railway project names renamed (MusicGen-DB, AudioStudio-DB)

## Step 1: Collect DATABASE_URLs

### Option A: Manual (from Railway Dashboard)
1. Go to https://railway.app
2. Click each project: MusicGen-DB and AudioStudio-DB
3. Navigate to Environment Variables
4. Copy the `DATABASE_URL` for each

### Option B: Automated (via script)
```bash
# First get project IDs
railway project ls --json | jq '.projects[] | {name: .name, id: .id}'

# Then run collection script
python3 scripts/collect_railway_db_urls.py --project-id <project_id> --project-id <project_id>
```

## Step 2: Populate the Template

Copy DATABASE_URLs to `docs/railway_db_urls_template.json`:

```json
{
  "MusicGen": "postgres://user:password@railway.internal:5432/musicgen_db?sslmode=require",
  "AudioStudio": "postgres://user:password@railway.internal:5432/audiostudio_db?sslmode=require"
}
```

**Note:** Project names must match your Vercel project names exactly.

## Step 3: Run Automation

```bash
cd ~/.openclaw/workspace
python3 scripts/auto_vercel_db.py --config docs/railway_db_urls_template.json
```

This will:
1. Authenticate with Vercel API
2. Find projects matching names in your JSON
3. Set DATABASE_URL environment variables
4. Trigger automatic deployments

## Step 4: Verify Connection

Check Vercel project logs for errors, or test the application:
- MusicGen: https://edmmusic.studio
- AudioStudio: https://audiostudio.ai

---
**Estimated time:** 15-20 minutes
**Dependencies:** Vercel API token (pre-configured)
