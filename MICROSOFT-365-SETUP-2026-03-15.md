# Microsoft 365 CLI Setup - Progress Document

**Date:** 2026-03-15  
**Status:** In Progress (Microsoft 365 OAuth setup pending)  
**Account:** support@zer0daylabs.com (Office 365 hosted by GoDaddy)

---

## Problem Identified

**Heartbeat Alert (2026-03-15 07:36 MST):**
- ❌ **Calendar OAuth expired** - tokens need re-auth
- ❌ **Inbox (Gmail) OAuth expired** - tokens need re-auth
- ⚠️ **GitHub rate limit hit** - authentication issue
- ✅ **Vercel** - token valid (`support-9645`)
- ✅ **Railway** - authenticated (`support@zer0daylabs.com`)

**Root Cause:** Zer0Day Labs uses `support@zer0daylabs.com` which is **Microsoft 365 (Office 365)** hosted by GoDaddy, not Google Workspace. The `gog` CLI only supports Google Workspace.

---

## Research & Options Evaluated

### What We Found

1. **`gog` CLI** (already installed) = Google Workspace ONLY
   - Handles: Gmail, Calendar, Drive, Sheets, Docs, etc.
   - ❌ Does NOT support Microsoft 365

2. **Microsoft 365 Options Evaluated:**

#### **Option A: `clippy` (Microsoft 365 CLI) - ✅ SELECTED**
- **Package:** `@pnp/cli-microsoft365` (v11.5.0)
- **ClawHub:** [clippy](https://clawhub.com/skills/clippy) (3.690 rating)
- **Capabilities:**
  - ✅ Exchange Online (Email/Outlook)
  - ✅ Microsoft Graph (Calendar, OneDrive, SharePoint)
  - ✅ Azure AD management
  - ✅ OAuth authentication
- **Maintainer:** PnP (Microsoft Community)

#### **Option B: `outlook-email` (ClawHub)**
- Rating: 1.102
- Focused on email operations only
- Less comprehensive than full M365 CLI

#### **Option C: IMAP/SMTP via `himalaya`**
- Rating: 1.150
- ✅ Already installed
- ✅ Basic email operations
- ❌ No calendar support
- ❌ IMAP-only (basic operations)

**Decision:** Go with `clippy` (Option A) - most comprehensive, matches `gog` philosophy.

---

## Implementation Progress

### ✅ Completed (2026-03-15 10:20 MST)

1. **Installed Microsoft 365 CLI**
   ```bash
   npm i -g @pnp/cli-microsoft365
   ```
   - Version: 11.5.0
   - Installed: 400 packages

2. **Verified installation**
   - ✅ `m365 --version` works
   - ✅ CLI shows all commands (outlook, graph, entra, etc.)
   - ✅ Supports deviceCode, browser, password, certificate, oauth auth types

3. **Explored authentication methods**
   - `--authType deviceCode` - requires app registration
   - `--authType browser` - requires app registration
   - `--authType password` - requires password input, stores in keyring
   - `--authType secret` - requires client secret from app registration

### 🔄 Pending Decisions

**Authentication Strategy:**

**Path A: OAuth + Microsoft Entra App (Recommended for long-term)**
- Create Microsoft Entra app registration
- Grant API permissions (Mail.ReadWrite, Calendars.ReadWrite, etc.)
- Use app ID + OAuth authentication
- More secure, no passwords stored
- Requires admin consent for some permissions

**Path B: Password-based OAuth (Quick start)**
- Direct `m365 login --authType password` 
- Stores password in OS keyring (not files)
- Faster setup, less secure
- Password required on each login session

**Path C: Use existing `himalaya` (Workaround)**
- Keep IMAP/SMTP for email
- No calendar support via CLI
- Already working, minimal changes

---

## Next Steps Required

### To Complete OAuth Setup (Path A):

**Step 1: Create Microsoft Entra App Registration**
1. Go to [Microsoft Entra Admin Center](https://entra.microsoft.com/)
2. Navigate to **Identity > Apps > App registrations**
3. Click **"+ New registration"**
4. Fill in:
   - **Name:** `Zer0Day Labs CLI` (or custom name)
   - **Supported account types:** `Accounts in this organizational directory only`
   - **Redirect URI:** `Public client (mobile & desktop)` → `https://login.microsoftonline.com/common/oauth2/nativeclient`
5. Click **Register**
6. **Copy the Application (client) ID** (appears on app's overview page)

**Step 2: Grant API Permissions**
1. Go to **API permissions** → **"+ Add a permission"**
2. Select **Microsoft Graph**
3. Add **Application permissions:**
   - `Mail.ReadWrite`
   - `Mail.Send`
   - `Calendars.ReadWrite`
   - `Files.ReadWrite`
4. Click **"Grant admin consent"** for your tenant
5. Note: May require global admin approval

**Step 3: Configure CLI**
Once app registration is complete with **Application ID** copied, run:
```bash
m365 login --appId <APP_ID> --tenant organizations --authType deviceCode
```

### To Complete Password Auth (Path B):

Run:
```bash
m365 login --authType password --userName support@zer0daylabs.com
```
- Will prompt for password
- Password stored securely in OS keyring
- No files modified

### To Test Email/Calendar Operations:

**Email (Exchange Online):**
```bash
# List messages
m365 outlook message list --count 10

# Search inbox
m365 outlook message search --query 'isRead:false'

# Send email
m365 outlook mail send --to "recipient@example.com" --subject "Test" --body "Hello"
```

**Calendar (Microsoft Graph):**
```bash
# List events
m365 graph calendar event list

# Create event
m365 graph calendar event add --subject "Test Event" --start "2026-03-15T10:00:00" --end "2026-03-15T11:00:00"
```

---

## Files Created/Modified

**New:**
- `~/.openclaw/workspace/MICROSOFT-365-SETUP-2026-03-15.md` (this file)
- Global package: `@pnp/cli-microsoft365@11.5.0`

**Existing (unchanged):**
- `.m365rc.json` - Not yet created (will be created after setup)
- OS keyring - Password storage (if using password auth)

---

## Configuration Commands (For Future Reference)

### Device Code Authentication (No app registration):
```bash
# This requires creating a Microsoft Entra app first
m365 login --authType deviceCode --userName support@zer0daylabs.com
# Note: Still requires appId, but simpler flow
```

### Password Authentication (Quick setup):
```bash
# One-time setup, stores password in keyring
m365 login --authType password --userName support@zer0daylabs.com
# You'll be prompted for password, stored in OS keyring
```

### OAuth Browser Authentication:
```bash
# Opens browser for login flow
m365 login --authType browser --userName support@zer0daylabs.com
```

### Check Connection Status:
```bash
m365 status
```

### Log Out:
```bash
m365 logout
```

---

## Decision Summary

**Current Choice:** 
- Tool: `@pnp/cli-microsoft365` (v11.5.0)
- Account: `support@zer0daylabs.com`
- Auth Method: **Pending** (OAuth + app registration recommended)

**Recommendation:** 
Proceed with **OAuth + app registration** (Path A) for long-term security. 
This is more complex initially but avoids password storage and is more secure.

**If urgent:** Use password auth (Path B) for quick setup.

---

## Related Documentation

- **CLI for Microsoft 365 Official Docs:** https://pnp.github.io/cli-microsoft365/
- **Installation Guide:** https://pnp.github.io/cli-microsoft365/user-guide/installing-cli/
- **Authentication Guide:** https://pnp.github.io/cli-microsoft365/user-guide/connecting-microsoft-365/
- **Microsoft Entra App Registration:** https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

---

*Document created by CB - Zer0Day Labs AI Partner*
*Last updated: 2026-03-15 10:26 MST*
