### Microsoft 365 OAuth Setup - Decision Framework

**Status:** ⏸️ Pending Lauro's decision on authentication method  
**Priority:** HIGH (Calendar/Inbox automation blocked)  
**Account:** support@zer0daylabs.com (Office 365, GoDaddy hosted)

---

## Current State

**Tool Installed:** `@pnp/cli-microsoft365` v11.5.0 ✅  
**Authentication:** NOT configured  
**CLI Status:** Logged out

---

## Options Evaluated

### Option A: OAuth + Microsoft Entra App (Recommended - Long-term Security)

**Steps Required:**
1. Create Entra app registration at [entra.microsoft.com](https://entra.microsoft.com)
2. Grant API permissions (Mail.ReadWrite, Calendars.ReadWrite, etc.)
3. Grant admin consent
4. Use `m365 login --appId <APP_ID> --tenant organizations --authType deviceCode`

**Pros:**
- ✅ More secure - no passwords stored
- ✅ Standard enterprise authentication
- ✅ Works with MFA/conditional access
- ✅ Can rotate without exposing credentials
- ✅ Audit trail via Azure AD logs

**Cons:**
- ⚠️ Requires admin consent for some permissions
- ⚠️ More steps (15-20 minutes setup)
- ⚠️ Requires Microsoft 365 admin access

**Effort:** 15-20 minutes (one-time setup)

---

### Option B: Password-based OAuth (Quick Start)

**Steps Required:**
1. Run: `m365 login --authType password --userName support@zer0daylabs.com`
2. Enter password (stored in OS keyring, not files)
3. Start automating Calendar/Inbox

**Pros:**
- ✅ Fast setup (1-2 minutes)
- ✅ No admin access required
- ✅ Immediate automation capability

**Cons:**
- ⚠️ Password stored in keyring
- ⚠️ Less secure (password in plaintext in OS)
- ⚠️ Requires MFA bypass or app password
- ⚠️ MFA may block login depending on tenant policy

**Effort:** 2-5 minutes (one-time setup)

---

### Option C: Use Existing Himaya CLI (Partial Solution)

**Steps Required:**
1. Use `himalaya` for email operations (IMAP/SMTP)
2. No calendar support via CLI
3. Keep calendar automation manual

**Pros:**
- ✅ Already installed
- ✅ No new credentials needed
- ✅ Email operations work immediately

**Cons:**
- ❌ No calendar automation
- ❌ Limited to basic IMAP operations
- ❌ Missing full M365 feature set

**Effort:** 0 minutes (already in place)

---

## Recommendation

**For Zer0Day Labs (security-focused):**  
**Choose Option A (OAuth + Entra App)** - 15-20 minutes

**Rationale:**
- Zer0Day Labs handles sensitive client data
- Security-conscious culture
- Long-term infrastructure investment
- No need to store passwords
- Audit trail important for compliance

**If urgent timeline:**  
**Choose Option B (Password Auth)** - 2-5 minutes

---

## Next Actions Required

**Decision needed from Lauro:**
1. **Option A (Recommended):** Proceed with Entra app registration
   - Need Microsoft 365 admin access
   - Estimated time: 15-20 min
   - Outcome: Full M365 CLI automation, secure

2. **Option B (Quick):** Use password auth
   - No admin access needed
   - Estimated time: 2-5 min
   - Outcome: Immediate automation, less secure

3. **Option C (Partial):** Keep himalaya only
   - Email automation only
   - Estimated time: 0 min
   - Outcome: Calendar automation manual

---

## Implementation Commands (After Decision)

### If Option A (OAuth + App):
```bash
# Create Entra app, get APP_ID
# Then:
m365 login --appId <APP_ID> --tenant organizations --authType deviceCode
```

### If Option B (Password):
```bash
m365 login --authType password --userName support@zer0daylabs.com
# Will prompt for password, stored in OS keyring
```

### Test After Authentication:
```bash
# Check connection
m365 status

# Test email
m365 outlook message list --count 3

# Test calendar
m365 graph calendar event list
```

---

*Decision needed: Option A or Option B? Document in task #53 when ready to proceed.*
