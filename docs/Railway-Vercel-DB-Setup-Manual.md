# Railway ↔ Vercel DATABASE_URL Integration

## Task Status: BLOCKED - Requires Manual Action

**Project ID:** e08a6f57-1e45-490b-8a5e-bfd1c6778ebb (AudioStudio-DB)
**Project ID:** dea04097-ee82-4f7a-9766-30fbe718ff72 (MusicGen-DB)

---

## Why Manual Action Required

The Railway GraphQL API is blocked by Cloudflare. Must collect DATABASE_URLs via dashboard.

---

## Instructions (5 minutes)

### Step 1: Login to Railway
1. Go to https://railway.app
2. Login as support@zer0daylabs.com

### Step 2: Collect DATABASE_URL from MusicGen-DB
1. Navigate to **Projects** → **zer0day** workspace
2. Click on **MusicGen-DB** project
3. Go to **Variables** tab (or Environment Variables)
4. Find the variable named `DATABASE_URL`
5. **Copy the entire connection string** (e.g., `postgres://user:password@host:5432/dbname?sslmode=require`)

### Step 3: Collect DATABASE_URL from AudioStudio-DB
1. Click on **AudioStudio-DB** project
2. Go to **Variables** tab
3. Find the variable named `DATABASE_URL`
4. **Copy the entire connection string**

### Step 4: Update the Mapping File

Open `~/.openclaw/workspace/scripts/railway_db.json` and paste the values:

```json
{
  "MusicGen": "POSTED_MUSICGEN_DATABASE_URL_HERE",
  "AudioStudio": "POSTED_AUDIOSTUDIO_DATABASE_URL_HERE"
}
```

### Step 5: Run the Automation Script

```bash
cd ~/.openclaw/workspace
python3 scripts/auto_vercel_db.py --config scripts/railway_db.json
```

This will automatically:
- Match Railway projects to Vercel deployments
- Set DATABASE_URL environment variables
- Trigger deployments

### Step 6: Verify
1. Check Vercel dashboard for successful deployments
2. Verify no database connection errors in logs
3. Test application functionality (loop generation, etc.)

---

## Expected Results

**MusicGen (edmmusic.studio):**
- DATABASE_URL configured from MusicGen-DB
- Should connect to PostgreSQL
- Loop generation, user data storage working

**AudioStudio (audiostudio.ai):**
- DATABASE_URL configured from AudioStudio-DB
- User data, subscriptions connected
- No "database not configured" errors

---

## Risk Assessment

- **Risk Level:** Low
- **Scope:** Only Vercel ↔ Railway connection
- **Reversible:** Easy - just remove DATABASE_URL env var in Vercel
- **Impact:** Applications won't save user data without DB connection

---

## Notes

- Railway projects already renamed: MusicGen-DB, AudioStudio-DB
- No migration needed - existing data in Railway DBs
- Credentials are secure in Railway, no password sharing needed
- Estimated time: 10-15 minutes (including verification)
