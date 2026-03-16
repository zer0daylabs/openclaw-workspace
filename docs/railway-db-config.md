# Railway Database URLs Configuration

This file provides the DATABASE_URL values for connecting MusicGen and AudioStudio to their Railway PostgreSQL databases.

## How to Get DATABASE_URL from Railway

1. Log in to Railway dashboard: https://railway.app
2. Navigate to **Projects** → **MusicGen** project (or the relevant project)
3. Click **Settings** → **Environment Variables**
4. Copy the value of `DATABASE_URL` (or `CONNECTION_STRING`)
5. Paste it into `railway_db.json`

## Required Values

| Field | Railway Project | Description |
|--|--|--|-----|
| `MusicGen` | `MusicGen-DB` (formerly `lucky-playfulness`) | PostgreSQL connection string for EDM Music Studio |
| `AudioStudio` | `AudioStudio-DB` (formerly `new-db-app`) | PostgreSQL connection string for AudioStudio |

## Next Steps

1. **Fill in the URLs** in `scripts/railway_db.json`
2. **Execute** the automation script:
   ```bash
   python3 scripts/auto_vercel_db.py --config scripts/railway_db.json
   ```
3. **Verify** that MusicGen and AudioStudio are connecting to the databases
4. **Test** by making a request to each app and checking for successful DB operations

## Example DATABASE_URL Format

```
postgres://user:password@host:5432/database_name?sslmode=require
```

**Note:** Railway PostgreSQL connection strings include SSL mode and are secure for production use.
