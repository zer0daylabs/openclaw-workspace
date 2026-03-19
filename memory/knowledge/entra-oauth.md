# Microsoft 365 / Entra OAuth — CB Knowledge Summary

Last updated: 2026-03-19
Proficiency: aware → basic (research complete)
Domain: Authentication, OAuth 2.0, SSO

---

## What It Is

**Microsoft Entra ID** (formerly Azure Active Directory) is Microsoft's cloud-based identity and access management service. For Zer0Day Labs use case:
- Provides **OAuth 2.0 + OpenID Connect** authentication
- Enables **single sign-on (SSO)** for users
- Issues **JWT-based security tokens** (Access tokens, ID tokens, Refresh tokens)
- Used for securing applications like **MusicGen, AudioStudio**
- Replaces custom auth with enterprise-grade authentication

**Azure AD vs. Microsoft 365**:
- Azure AD is the identity platform
- Microsoft 365 includes Azure AD (for user management)
- Both share the same underlying identity infrastructure

---

## Key Concepts

### OAuth 2.0 Roles

1. **Authorization Server** - Microsoft Entra ID (identity provider/IdP)
2. **Client** - Your application (MusicGen, AudioStudio)
3. **Resource Owner** - The end user who "owns" their data
4. **Resource Server** - The API/Web API that hosts protected resources

### Token Types

1. **Access Tokens** - JWT with permissions to access resources
2. **ID Tokens** - Contains user basic information (email, name, user ID)
3. **Refresh Tokens** - Long-lived tokens to request new access tokens (sensitive!

---

## App Registration (Required Setup)

Before integrating, you must **register your application**:

1. Navigate to **Microsoft Entra admin center** → **App registrations**
2. Click **"New registration"**
3. Fill in:
   - **Name**: Your app name (e.g., "MusicGen Auth")
   - **Supported account types**: Choose who can sign in
     - `Accounts in this organizational directory only` (single tenant)
     - `Accounts in any organizational directory` (multi-tenant)
     - `Accounts in any organizational directory and personal Microsoft accounts` (broad)
   - **Redirect URI**: URL where auth responses will be sent

### Redirect URI Configuration

For **Next.js web apps**, use:
```
Development: http://localhost:3000/api/auth/callback/azure-ad
Production:  https://yourdomain.com/api/auth/callback/azure-ad
```

**Important**: Redirect URI must **exactly match** one registered in the portal.

### Required Settings

After registration, note these values:

1. **Application (client) ID** - Unique identifier for your app
2. **Directory (tenant) ID** - Your tenant identifier
3. **Client secret** - Generate under "Certificates & secrets"
   - Creates a password-like secret (store securely!)
4. **API permissions** - Configure what your app can access (Graph API, etc.)

---

## Endpoints

Microsoft identity platform provides standard OAuth 2.0 + OIDC endpoints:

```http
# Authorization endpoint (user signs in)
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize

# Token endpoint (exchange code for tokens)
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token

# User info endpoint (get profile details)
https://graph.microsoft.com/oidc/userinfo
```

**Tenant values**:
- `common` - Microsoft accounts + work/school accounts
- `organizations` - Work/school accounts only
- `consumers` - Microsoft accounts only
- `tenant-id` - Specific tenant (most secure)
- `domain-name` - Custom domain (e.g., `zer0daylabs.onmicrosoft.com`)

---

## Next.js Integration

### Using NextAuth.js (Recommended)

**NextAuth.js** is the industry-standard auth framework for Next.js:

```bash
npm install next-auth@beta
```

**Configuration** (`/app/api/auth/[...nextauth]/route.ts`):

```typescript
import NextAuth from 'next-auth'
import AzureADProvider from 'next-auth/providers/azure-ad'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    AzureADProvider({
      clientId: process.env.AUTH_AZUREAD_CLIENT_ID,
      clientSecret: process.env.AUTH_AZUREAD_CLIENT_SECRET,
      tenantId: process.env.AUTH_AZUREAD_TENANT_ID,
    }),
  ],
  callbacks: {
    async jwt({ token, account, profile }) {
      // Store access token in JWT
      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },
    async session({ session, token }) {
      // Add access token to session
      session.accessToken = token.accessToken
      return session
    },
  },
})
```

**Environment Variables** (`.env.local`):
```env
AUTH_AZUREAD_CLIENT_ID=<App registration client ID>
AUTH_AZUREAD_CLIENT_SECRET=<App registration client secret>
AUTH_AZUREAD_TENANT_ID=<Directory (tenant) ID>
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Manual Implementation (Not Recommended)

For manual OAuth flow, implement:

1. **Authorization Request**:
```url
https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?
  client_id={client_id}
  &response_type=code
  &redirect_uri={redirect_uri}
  &scope=https://graph.microsoft.com/User.Read
  &state={state}
  &code_challenge={code_challenge}
  &code_challenge_method=S256
```

2. **Token Exchange**:
```bash
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
code={authorization_code}
client_id={client_id}
client_secret={client_secret}
redirect_uri={redirect_uri}
```

**PKCE** (Proof Key for Code Exchange) is **required** for security - prevents authorization code interception attacks.

---

## Scopes & Permissions

### Built-in Scopes (OpenID Connect)

| Scope | Description |
|-------|-------------|
| `openid` | Required - get ID token |
| `profile` | Get user profile (name, email, etc.) |
| `email` | Get user email address |
| `offline_access` | Get refresh token |

### Microsoft Graph Scopes

To access Microsoft 365 services:

| Scope | Description | Type |
|-------|-------------|------|
| `User.Read` | Read user profiles | Delegated |
| `User.ReadBasic.All` | List all users | Delegated |
| `Mail.Read` | Read user mail | Delegated |
| `Calendars.Read` | Read user calendars | Delegated |
| `Directory.Read.All` | Read directory data | Delegated/Admin |

### Permission Types

1. **Delegated permissions** - Act as signed-in user (most common)
2. **Application permissions** - App has its own identity (no user context)

### Consent & Admin Approval

- Some permissions require **user consent** during first login
- Some permissions require **admin consent** (e.g., Directory.Read.All)
- Admin must approve in Azure AD admin center → Enterprise applications

---

## Next.js Pages Router Callback

The callback endpoint structure for Next.js Pages Router:

**File**: `pages/api/auth/[...nextauth].ts`

```typescript
import NextAuth from 'next-auth'
import AzureADProvider from 'next-auth/providers/azure-ad'

export default NextAuth({
  providers: [
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID,
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET,
      tenantId: process.env.AZURE_AD_TENANT_ID,
    }),
  ],
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.accessToken = token.accessToken
      }
      return session
    },
  },
})
```

**App Router Callback** (`/app/api/auth/[...nextauth]/route.ts`):

```typescript
import NextAuth from 'next-auth'
import AzureADProvider from 'next-auth/providers/azure-ad'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID,
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET,
      tenantId: process.env.AZURE_AD_TENANT_ID,
    }),
  ],
  session: { strategy: 'jwt' },
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.accessToken = token.accessToken
      }
      return session
    },
  },
})
```

---

## Our Use Case for Zer0Day Labs

**Current status**: OAuth setup started but not completed

**Integration goals**:
1. Provide **enterprise SSO** for MusicGen and AudioStudio users
2. Replace/reduce email-password auth with Microsoft accounts
3. Enable team-based access for organizations
4. Simplify user management (automatic account provisioning)

**Implementation plan**:
1. Create Azure AD app registration for MusicGen
2. Configure redirect URIs (localhost + production)
3. Set up API permissions (User.Read, email, profile)
4. Implement NextAuth.js in MusicGen (Next.js app)
5. Test authentication flow
6. Deploy and configure production URLs
7. Repeat for AudioStudio

**User journey**:
1. User clicks "Sign in with Microsoft" on MusicGen
2. Redirected to Microsoft login page
3. User enters Microsoft credentials
4. Granted consent (first time only)
5. Returned to MusicGen with JWT token
6. Session established, user authenticated

---

## Gotchas & Best Practices

### Common Issues

1. **Redirect URI mismatch** - Must match exactly (including trailing slash)
2. **Client secret expires** - Set reminder to renew before expiration
3. **CORS errors in SPA** - Configure redirect URI type as `spa` in portal
4. **API permissions not granted** - Admin must consent for certain permissions
5. **Token expiration** - Refresh tokens needed for long sessions
6. **Multi-tenant vs single-tenant** - Choose during registration (can't change later)

### Best Practices

1. **Use PKCE** - Always for mobile/SPA apps
2. **Store client secrets securely** - Use Azure Key Vault or similar
3. **Use JWT-based sessions** - No database needed
4. **Handle token refresh** - Implement refresh token logic
5. **Validate ID token signature** - Ensure tokens issued by trusted party
6. **Use minimal permissions** - Principle of least privilege
7. **Test both development and production** - Different redirect URIs
8. **Document tenant ID** - Store in environment variables, not code

### Security Considerations

1. **Never expose client secrets** in client-side code
2. **Use HTTPS** for all production redirect URIs
3. **Implement CSRF protection** - state parameter in authorization request
4. **Validate token expiration** - Don't trust token claims blindly
5. **Store tokens in httpOnly cookies** - Prevent XSS token theft
6. **Rotate secrets regularly** - At least annually

---

## Implementation Checklist

**Phase 1: Azure AD Setup**
- [ ] Create app registration in Entra admin center
- [ ] Configure redirect URIs (localhost + prod)
- [ ] Generate client secret (store securely)
- [ ] Configure API permissions (User.Read, email, profile)
- [ ] Get admin consent (if required)
- [ ] Note: Client ID, Tenant ID, Client Secret

**Phase 2: Application Setup**
- [ ] Install NextAuth.js (`npm install next-auth@beta`)
- [ ] Create `/app/api/auth/[...nextauth]/route.ts`
- [ ] Configure AzureADProvider with environment variables
- [ ] Implement JWT callbacks for token storage
- [ ] Create sign-in/sign-out pages
- [ ] Protect routes with `auth()` callback

**Phase 3: Testing**
- [ ] Test localhost authentication flow
- [ ] Verify token exchange works
- [ ] Check session persistence
- [ ] Test token refresh
- [ ] Test on production URL

**Phase 4: Deployment**
- [ ] Deploy app with Azure AD environment variables
- [ ] Update production redirect URI in Azure AD
- [ ] Test end-to-end flow
- [ ] Monitor authentication logs

---

## Resources

- **Microsoft Learn**: https://learn.microsoft.com/en-us/entra/identity-platform/
- **OAuth 2.0 Protocol Reference**: https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols
- **Authorization Code Flow**: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- **NextAuth.js Azure AD Provider**: https://next-auth.js.org/providers/azure-ad
- **Microsoft Graph API**: https://learn.microsoft.com/en-us/graph/permissions-reference
- **Azure AD App Registration Guide**: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

---

## Next Steps for Zer0Day Labs

**Priority**: Moderate - enhances security, provides enterprise features

**Current State**: Setup started but not completed

**Immediate Actions**:
1. Create Azure AD app registration for MusicGen
2. Document Client ID, Tenant ID, Client Secret
3. Install NextAuth.js in MusicGen repository
4. Configure authentication providers
5. Test local development flow
6. Deploy and configure production URLs
7. Repeat for AudioStudio

**Estimated Effort**: 2-3 hours for implementation + 1 hour testing
