# Railway Dashboard Cleanup Instructions

These steps will guide Lauro through the manual cleanup of unused Railway projects and renaming of cryptic projects so that the environment is clean and easier to maintain.

## Prerequisites
- Railway CLI installed and authenticated as **support@zer0daylabs.com** (token in `~/.openclaw/workspace/.credentials/railway.json`).
- Access to the Railway web dashboard (https://railway.app). Lauro must be logged in with the same account.

## Step 1: Open the Railway Dashboard
1. Navigate to https://railway.app.
2. Sign in with the **support@zer0daylabs.com** credentials.
3. From the dashboard, click **Projects** in the sidebar.

## Step 2: Identify Unused Projects to Delete
The following projects are unused DBs and should be removed:
1. **truthful-warmth** (Project ID: `4b9635d2-aed0-4464-b6f5-b1386123ddd9`)
2. **appealing-laughter** (Project ID: `3cafd6b5-75b8-4fa7-9ade-abe946180450`)

### Deleting the Projects
- For each project:
  1. Click the project name.
  2. In the project view, click **Settings** → **Danger Zone**.
  3. Click **Delete Project**.
  4. Confirm the deletion when prompted.
- Verify that both projects no longer appear in the project list.

## Step 3: Rename Cryptic Projects
The following projects have cryptic names that should be renamed to reflect their purpose:
1. **lucky-playfulness** → **MusicGen-DB** (Project ID: `dea04097-ee82-4f7a-9766-30fbe718ff72`)
2. **new-db-app** → **AudioStudio-DB** (Project ID: `561b9e81-07d2-4309-98dd-69a26deaa056`)

### Renaming the Projects
- For each project:
  1. Click the project name.
  2. In the project view, click **Settings** → **Rename Project**.
  3. Enter the new name and save.
  4. Verify that the new name appears in the project list.

## Step 4: Verify Database Connections
After renaming, confirm that the database services are still functioning:
1. In the Railway dashboard, click each renamed project.
2. Under **Services**, ensure the **Postgres** service is running.
3. Note the connection string (DATABASE_URL) displayed in the **Environment Variables** section.

## Step 5: Update Vercel Environment Variables
The Railway DB connection strings must be added to the Vercel projects for MusicGen and AudioStudio.
- For each Vercel project (MusicGen, AudioStudio):
  1. Go to the Vercel dashboard.
  2. Select the project.
  3. Navigate to **Settings** → **Environment Variables**.
  4. Add or update the `DATABASE_URL` variable with the value copied from Railway.
  5. Save and redeploy the project.

## Step 6: Final Verification
1. Confirm that both Vercel projects are running without database errors.
2. Check the logs on Railway and Vercel for any connection errors.
3. Ensure that the old projects (`truthful-warmth`, `appealing-laughter`) are fully deleted.

---
**Note:** These changes may require a brief restart of the deployed services to apply new environment variables.

---
If you encounter any issues, please capture the error messages and share them with the dev team for further assistance.
