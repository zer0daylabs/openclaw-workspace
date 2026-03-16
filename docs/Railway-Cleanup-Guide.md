# Railway Database Cleanup Guide

## Task: Delete Unused Railway Projects

**Account:** support@zer0daylabs.com
**Projects to delete:**
- `truthful-warmth` (ID: 4b9635d2-aed0-4464-b6f5-b1386123ddd9) - unused DB
- `appealing-laughter` (ID: 3cafd6b5-75b8-4fa7-9ade-abe946180450) - unused DB

## Verification Before Deletion ✅

**No data dependencies:**
- Both projects have NO services connected
- No Railway deployments depend on these DBs
- Not linked to Vercel applications
- Safe to delete

## Steps (5 minutes)

### Step 1: Login to Railway Dashboard
1. Go to https://railway.app
2. Login as support@zer0daylabs.com
3. Navigate to **Projects** → **zer0day** workspace

### Step 2: Delete truthful-warmth
1. Click on `truthful-warmth` project
2. Go to **Settings** tab
3. Scroll to **Danger Zone**
4. Click **Delete Project**
5. Type the project name to confirm
6. Click **Confirm Delete**

### Step 3: Delete appealing-laughter
1. Click on `appealing-laughter` project
2. Go to **Settings** tab
3. Scroll to **Danger Zone**
4. Click **Delete Project**
5. Type the project name to confirm
6. Click **Confirm Delete**

### Step 4: Verify Cleanup
1. Refresh Projects list
2. Confirm only these 5 projects remain:
   - MusicGen-DB
   - AudioStudio-DB
   - SlackBot
   - audio-converter
   - user-data-subscriptions

## Benefits
- **Reduced clutter:** Easier to find active projects
- **Cost savings:** Freeing up unused DB resources
- **Better organization:** Cleaner workspace

## Risk Assessment
- **Risk Level:** Very Low
- **Reversible:** NO (permanent deletion)
- **Impact:** None - no active deployments or integrations

## Estimated Time
**5-10 minutes** for both deletions

---
**Action required:** Lauro to execute manual dashboard cleanup
