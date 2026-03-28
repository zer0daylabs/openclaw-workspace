# MusicGen Pricing Page Deployment Checklist

**Date:** 2026-03-28  
**Status:** Ready for Deployment

---

## 📦 What's Being Deployed

### Files Changed in `repos/MusicGen/`
1. **Pricing page update** (`src/app/(marketing)/pricing/page.tsx`)
   - 4 tiers displayed: Free/$0, Pro/$14.99, Pro+/$19.99, Studio/$49.99
   - Annual billing with ~17% discount
   - Conversion optimization features

2. **Feature gating system** (`src/lib/feature-flags.ts`)
   - 248 lines of upgrade logic
   - Smart prompts for Pro/Pro+ tier features
   - Projects, Sets, API access, custom sample packs

3. **PostHog analytics** (`src/instrumentation.ts`, `src/lib/pricing-analytics.ts`)
   - 10+ tracking events for conversion optimization
   - A/B test readiness

4. **Pricing config** (`src/config/pricing.ts`)
   - Updated tier structure
   - Annual billing integration

---

## 🚀 Deployment Steps (Manual - Git Auth Unavailable)

### Step 1: Pull Code Locally
```bash
cd ~/.openclaw/workspace/repos/MusicGen
# Code already up to date locally
git log --oneline -3
# Should show:
# 931aae0 cb: Add PostHog analytics for pricing page conversion tracking
# 90cc702 cb: Implement feature gating system for Pro/Pro+ tier upgrades
# 7e06add cb: Implement new pricing structure - 4 tiers with Free/Pro/Studio
```

### Step 2: Configure PostHog Environment Variables
**You'll need to create a PostHog account first:**
1. Go to https://posthog.com/signup
2. Create a new project: "MusicGen Analytics"
3. Copy `NEXT_PUBLIC_POSTHOG_KEY` and `POSTHOG_API_KEY`

**Add to Vercel Environment Variables:**
```env
NEXT_PUBLIC_POSTHOG_KEY=phc_XXX  # From PostHog project settings
POSTHOG_API_KEY=phc_XXX  # Same key for server-side
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
NEXT_PUBLIC_APP_URL=https://edmmusic.studio
```

### Step 3: Install posthog-js Dependency
```bash
cd ~/.openclaw/workspace/repos/MusicGen
npm install posthog-js posthog-node
npm install
```

### Step 4: Deploy to Vercel
**Option A - Via Vercel Dashboard:**
1. Go to https://vercel.com/zer0daylabs/edmmusic.studio
2. Click "Deployments" → "Import Project"
3. Select local commit `931aae0`
4. Add environment variables from Step 2
5. Click "Deploy"

**Option B - Via CLI:**
```bash
# Link project to Vercel
cd ~/.openclaw/workspace/repos/MusicGen
vercel link --token jWrPblHIloTZth3oZbqQ0hq1 --yes

# Deploy
vercel --token jWrPblHIloTZth3oZbqQ0hq1 --prod --yes
```

### Step 5: Configure Stripe Products
**In Stripe Dashboard:**
1. Go to https://dashboard.stripe.com/products
2. Create 3 new products:
   - **Pro Monthly** - $14.99/mo
   - **Pro+ Monthly** - $19.99/mo  
   - **Studio Monthly** - $49.99/mo
3. Create annual variants with ~17% discount
4. Copy `price_` IDs to update `src/config/pricing.ts` with real price IDs

### Step 6: Test Before Going Live
1. Navigate to https://edmmusic.studio/pricing
2. Verify all 4 tiers display correctly
3. Test upgrade flow (Pro → Pro+ → Studio)
4. Check PostHog events firing (use DevTools → PostHog console)
5. Test annual billing toggle

### Step 7: Launch A/B Test
**In PostHog Dashboard:**
1. Create feature flag: `pricing-ab-test`
2. Configure: 50% control (current pricing), 50% variant (new structure)
3. Set success metric: `subscription_completed`
4. Enable experiment

---

## ✅ Post-Deployment Monitoring

### First 24 Hours
- **Track:** Conversion rate (target: 1-2%)
- **Watch:** Any errors in PostHog → Sentry
- **Metric:** Free → Pro upgrade rate

### First Week
- **Analyze:** Which tier gets most clicks
- **Check:** A/B test statistical significance (need ~100 conversions)
- **Adjust:** If < 0.5% conversion, iterate on messaging

### First Month
- **Target:** $200-500 MRR (from $9.99 current)
- **Measure:** 0.2% → 2-5% conversion
- **Review:** Email onboarding sequence performance

---

## 📊 Success Metrics

| Metric | Current | Target (30 days) | Target (90 days) |
|--------|---------|---------------:|----------------:|
| MRR | $9.99 | $50 | $200-500 |
| Conversion rate | <0.2% | 2% | 5% |
| Free → Pro | - | 1:50 | 1:20 |
| Annual adoption | 0% | 30% | 50% |

---

## ⚠️ Rollback Plan

**If deployment fails or conversion drops:**
1. Go to Vercel Dashboard → Deployments
2. Click previous deployment (before pricing update)
3. Click "Promote"
4. Revert to old pricing structure
5. Notify Lauro immediately

---

## 📝 Notes

- **Estimated deployment time:** 15-30 minutes
- **Downtime:** None (Vercel deployments are zero-downtime)
- **Email onboarding:** Ready to deploy after pricing is live
- **Feature gating:** Already implemented, just needs Stripe integration
- **Documentation:** All in place (this checklist + pricing-page-spec.md)

---

## 🎯 Action Required

**Lauro needs to:**
1. Create PostHog account and project
2. Configure Stripe products (3 tiers + annual variants)
3. Deploy code to Vercel (use CLI or dashboard)
4. Add PostHog env vars to Vercel
5. Test pricing page live
6. Launch A/B test

**Estimated time:** 10-15 minutes for deployment, 30 minutes for Stripe setup

---

**Status:** ✅ Ready for deployment  
**Next step:** Manual Vercel deployment and Stripe configuration
