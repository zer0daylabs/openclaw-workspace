# PostHog — CB Knowledge Summary

Last updated: 2026-03-28
Proficiency: working (updated 2026-03-28 - implemented pricing analytics)
Domain: Product analytics, A/B testing, feature flags

---

## Implementation Status (2026-03-28)

### ✅ Implemented for MusicGen
1. **PostHog instrumentation** (`src/instrumentation.ts`)
   - Server-side SDK setup
   - Capture wrapper function
2. **Pricing analytics** (`src/lib/pricing-analytics.ts`)
   - Page view tracking
   - CTA click tracking
   - Conversion funnel tracking
   - Free tier limit tracking
   - Feature interest tracking (Projects, Sets, API, Custom sample packs)

### 📊 Events Tracked
- `pricing_page_view` - User visits pricing page with tier interest
- `pricing_cta_click` - User clicks upgrade button
- `pricing_upgrade_intent` - User considers upgrade
- `pricing_annual_toggle` - User switches billing cycle
- `pricing_comparison_table_view` - User views comparison table
- `pricing_faq_view` - User views FAQ topic
- `free_generation_limit_reached` - Free user hits 50 gen limit
- `first_project_created` - Tutorial trigger
- `sets_feature_interest` - Pro+ upgrade trigger
- `checkout_started/completed` - Conversion funnel

### 🎯 Next Steps
1. Install `posthog-js` in MusicGen dependencies
2. Add PostHog credentials to `.env` (NEXT_PUBLIC_POSTHOG_KEY, POSTHOG_API_KEY)
3. Configure reverse proxy for heatmaps
4. Create pricing A/B test flag in PostHog
5. Connect Stripe events to user IDs
6. Monitor for 1 week, analyze results


---

## What It Is

PostHog is a product analytics platform that combines:
- **Product analytics** (events, funnels, retention)
- **Feature flags** (rollouts, experiments)
- **A/B testing** (statistically rigorous experiments)
- **Session replays** (user behavior visualization)
- **Heatmaps** (click/tap tracking)
- **Error tracking** (frontend + backend errors)

All-in-one alternative to Segment + Google Analytics + Optimizely.

---

## Key Commands / Installation

### Manual Installation (Next.js App Router)

1. **Install SDK:**
```bash
npm install posthog-js
npm install posthog-node
```

2. **Environment variables:**
```env
NEXT_PUBLIC_POSTHOG_KEY=phc_xxx_project_token_from_dashboard
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```

3. **Create `instrumentation-client.ts`:**
```typescript
import posthog from 'posthog-js'

if (process.env.NEXT_PUBLIC_POSTHOG_KEY) {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
    person_profiles: 'identified_only',
  })
}
```

4. **Identify users:**
```typescript
posthog.identify(user_id) // after login
```

5. **Server-side:**
```typescript
import posthog from 'posthog-node'
const posthogClient = new PostHogClient({
  apiKey: process.env.POSTHOG_API_KEY,
  flushAt: 1, flushInterval: 0,
})
await posthogClient.capture({ distinctId: user_id, event: 'subscription_completed' })
```

---

## Integration Points

- **Next.js** (MusicGen, AudioStudio): Use instrumentation-client.ts for server-side bootstrapping
- **Stripe**: Track subscription events, link to user IDs
- **A/B Testing**: Create feature flags, run experiments with Bayesian stats

---

## Gotchas

1. Must call `posthog.identify()` after login to link user events
2. Next.js fetch cache may return stale feature flag values
3. WAF may block heatmaps - need IP allowlist (US: 44.205.89.55, 52.4.194.122, 44.208.188.173; EU: 3.75.65.221, 18.197.246.42, 3.120.223.253)
4. Use managed reverse proxy for better reliability vs browser blockers

---

## Our Use Case

**Goals:**
1. A/B test pricing ($9.99 → $14.99 → $19.99 → $49.99 Studio)
2. Test CTA variants on MusicGen/AudioStudio signup pages
3. Session replays to identify UX friction points
4. Measure conversion impact of changes

**Resources:**
- Docs: posthog.com/docs
- Next.js tutorial: posthog.com/tutorials/nextjs-ab-tests
- Wizard: github.com/PostHog/wizard

---

## Next Steps

1. Create PostHog Cloud account
2. Install SDK on MusicGen (edmmusic.studio)
3. Configure reverse proxy
4. Create pricing A/B test flag
5. Run tests for 1 week, analyze results
