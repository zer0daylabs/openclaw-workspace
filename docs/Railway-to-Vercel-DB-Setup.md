# Connecting Railway DBs to Vercel

## Overview
This guide walks through connecting Railway database projects to your Vercel-hosted applications (MusicGen, AudioStudio).

## Two Approaches:

### Option A: Manual Dashboard Collection (Recommended for one-time setup)
See steps below.

### Option B: Automated Collection via API
Use the script `scripts/collect_railway_db_urls.py` to fetch DATABASE_URLs programmatically:

```bash
python3 scripts/collect_railway_db_urls.py --project-id <project_id>
```

You can find project IDs by running:
```bash
railway project ls --json | jq '.projects[].id'
```

---

1. Log in to Railway Dashboard: https://railway.app
2. Navigate to **Projects**
3. For each project you want to use:

**MusicGen Database (`lucky-playfulness`)**
- Click on the project
- Go to **Environment Variables** or **Settings** → **Environment Variables**
- Find `DATABASE_URL` variable
- Copy the full connection string (e.g., `postgres://user:password@host:5432/dbname?sslmode=require`)

**AudioStudio Database (`new-db-app`)**
- Click on the project
- Go to **Environment Variables** or **Settings** → **Environment Variables**
- Find `DATABASE_URL` variable
- Copy the full connection string

## Step 2: Update the Mapping File

Open `~/.openclaw/workspace/docs/railway_db_urls_template.json` and replace the placeholder values:

```json
{
  "MusicGen": "postgres://actual_user:actual_password@actual_host:5432/actual_dbname?sslmode=require",
  "AudioStudio": "postgres://actual_user:actual_password@actual_host:5432/actual_dbname?sslmode=require"
}
```

## Step 3: Run the Automation Script

```bash
cd ~/.openclaw/workspace
python3 scripts/auto_vercel_db.py --config docs/railway_db_urls_template.json
```

This will:
1. List your Vercel projects
2. Match them by name (MusicGen, AudioStudio)
3. Set the DATABASE_URL environment variable for each
4. Trigger a Vercel deployment

## Step 4: Verify Connection

1. Check Vercel project logs after deployment
2. Verify no database connection errors
3. Test application functionality (loop generation, etc.)

## Troubleshooting

**Error: "Vercel project not found"**
- Ensure project names in the JSON match exactly (case-sensitive)
- Check Vercel project names in dashboard

**Error: "Database connection failed"**
- Verify Railway DB is running (check Railway project status)
- Check SSL mode settings match
- Ensure Railway allows connections from Vercel IPs

**Error: "Authentication failed"**
- Verify DATABASE_URL credentials are correct
- Check Railway user permissions

---
**Estimated time:** 10-15 minutes
**Manual effort required:** Collect DATABASE_URLs from Railway dashboard
