# Microsoft 365 OAuth Setup Guide

## Account: support@zer0daylabs.com

## Decision: App Registration (OAuth) vs Password Auth

**Recommendation: OAuth with app registration**
- More secure than password auth
- Can revoke access without changing password
- Works with MFA/SSO
- Required for modern Exchange Online

## Steps to Complete

### 1. Create Microsoft Entra App Registration
1. Go to https://portal.azure.com
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Name: `Zer0Day Labs - Microsoft 365 Integration`
5. Supported account types: `Accounts in this organizational directory only`
6. Redirect URI: None needed for CLI app
7. Click **Register**

### 2. Configure API Permissions
1. In app registration, go to **API permissions** → **Add a permission**
2. Select **Microsoft Graph**
3. Under **Delegated permissions**, add:
   - `Mail.Send`
   - `Mail.Read`
   - `Mail.ReadWrite`
   - `User.Read`
   - `Calendars.Read`
   - `Calendars.ReadWrite`
4. Click **Grant admin consent** for support@zer0daylabs.com

### 3. Create Client Secret
1. Go to **Certificates & secrets** → **New client secret**
2. Description: `CLI Access`
3. Expires: 12 months
4. **Copy the value immediately** (shown only once)

### 4. Save Credentials
Store in `~/.openclaw/workspace/.credentials/m365.json`:
```json
{
  "tenant_id": "YOUR_TENANT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET_VALUE",
  "user_email": "support@zer0daylabs.com"
}
```

### 5. Test Connection
Run a test to verify:
- IMAP connectivity (read emails)
- SMTP connectivity (send emails)
- Calendar permissions (if needed)

## CLI Tools That Will Use This
- Himilaya (email client)
- Calendar operations
- Any Microsoft 365 integration

## Risk Assessment
- Low risk: Only affects support@zer0daylabs.com
- Easy to revoke: Delete app registration to revoke all access
- No password sharing: OAuth tokens are time-limited

## Notes
- MFA is enabled on the account - OAuth bypasses this for CLI
- Support email already configured in system
- No shared passwords needed - credentials are encrypted locally
