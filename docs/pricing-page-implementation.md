# Pricing Page Implementation Checklist

## Overview
This document provides a step-by-step implementation guide for the MusicGen pricing page based on the specification in `docs/pricing-page-spec.md`.

**Target**: Implement pricing page that converts <0.2% → 2%+ conversion rate

---

## Phase 1: Setup (1-2 hours)

### 1.1 Create New Route
- **Location**: `/edmmusic.studio/app/pricing/page.tsx`
- **Framework**: Next.js App Router (based on existing structure)
- **Template**: Use existing layout components from homepage

### 1.2 Install Dependencies
```bash
cd ~/.openclaw/workspace/repos/MusicGen
npm install stripe
```

### 1.3 Set Up Stripe Webhook
- **Endpoint**: `/api/stripe/webhook`
- **Events to handle**: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`
- **Test mode first**: Use Stripe CLI for local testing

---

## Phase 2: UI Components (2-3 hours)

### 2.1 Create Pricing Card Components
```tsx
// pricing-page-spec.md shows 3-card layout
// Create reusable pricing-card.tsx component
// Props: tier, price, features, isAnnual, onSelect
```

**Components to create**:
1. `PricingTierCard.tsx` - Individual tier card
2. `PricingToggle.tsx` - Monthly/Annual toggle
3. `PricingComparisonTable.tsx` - Feature comparison table
4. `PricingFAQ.tsx` - FAQ accordion
5. `PricingCTA.tsx` - Bottom call-to-action

### 2.2 Implement Feature Lists
```tsx
// Use conditional rendering based on tier
// Example: 
{tier === 'pro' && <FeatureIcon icon="unlimited-loops">Unlimited Loops</FeatureIcon>}
```

### 2.3 Add Conversion Triggers
- **After 50 free loops**: Show "Upgrade to Pro" modal
- **Access Projects**: Show upgrade prompt
- **Create 5 Projects**: Show Pro+ upgrade prompt

---

## Phase 3: Stripe Integration (1-2 hours)

### 3.1 Create Products in Stripe Dashboard
1. **Pro Monthly**: $9.99/mo
2. **Pro Annual**: $99/year (17% discount)
3. **Pro+ Monthly**: $19.99/mo
4. **Pro+ Annual**: $199/year

### 3.2 Implement Checkout Sessions
```typescript
// /api/stripe/create-checkout.ts
export async function POST(req: Request) {
  const { tier, interval } = await req.json();
  const product = tier === 'pro' ? 'price_pro_monthly' : 'price_pro_plus_monthly';
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: product, quantity: 1 }],
    mode: 'subscription',
    success_url: 'https://edmmusic.studio/dashboard?success=true',
    cancel_url: 'https://edmmusic.studio/pricing?canceled=true',
  });
  return Response.json({ url: session.url });
}
```

### 3.3 Handle Webhooks
```typescript
// /api/stripe/webhook.ts
export async function POST(req: Request) {
  const sig = req.headers.get('stripe-signature');
  const event = stripe.webhooks.constructEvent(
    req.body, sig, process.env.STRIPE_WEBHOOK_SECRET
  );
  
  switch (event.type) {
    case 'checkout.session.completed':
      // Activate subscription features
      break;
    case 'customer.subscription.deleted':
      // Downgrade user to free tier
      break;
  }
}
```

---

## Phase 4: Feature Gating (1-2 hours)

### 4.1 Implement Feature Flags
```typescript
// lib/feature-flags.ts
export function hasFeature(userTier: 'free' | 'pro' | 'pro+', feature: string): boolean {
  const tiers = {
    free: ['loops', 'basic-controls', 'mp3-export'],
    pro: ['loops', 'basic-controls', 'mp3-export', 'wav-export', 'projects'],
    proPlus: ['loops', 'basic-controls', 'mp3-export', 'wav-export', 'flac-export', 'projects', 'sets', 'api-access']
  };
  return tiers[userTier]?.includes(feature) ?? false;
}
```

### 4.2 Protect Protected Routes
```tsx
// App router protection
function ProtectedRoute({ children, requiredTier }: { children: ReactNode, requiredTier: 'pro' | 'proPlus' }) {
  const userTier = useUserTier();
  if (!hasFeature(userTier, 'pro') && requiredTier === 'pro') {
    return <UpgradePrompt tier="pro" />;
  }
  return children;
}
```

---

## Phase 5: Analytics & Testing (1-2 hours)

### 5.1 Add PostHog Events
```typescript
// Track pricing page views
posthog.capture('pricing_page_view', { 
  tier_interest: 'pro' | 'proPlus', 
  billing: 'monthly' | 'annual' 
});

// Track conversion
posthog.capture('pricing_upgrade_click', { tier: 'pro', billing: 'annual' });
```

### 5.2 Testing Checklist
- [ ] Free tier user can view pricing page
- [ ] Pro tier upgrade flows work
- [ ] Pro+ upgrade flows work
- [ ] Annual toggle updates prices correctly
- [ ] Stripe webhook handles test events
- [ ] Feature gating works for Pro users
- [ ] Feature gating works for Pro+ users
- [ ] Conversion triggers appear after 50 loops
- [ ] Mobile responsive design

---

## Phase 6: Launch & Monitor (ongoing)

### 6.1 Go Live Steps
1. Switch Stripe to production mode
2. Deploy pricing page to Vercel
3. Enable feature gating for Pro/Pro+ users
4. Announce via email to existing free users

### 6.2 Success Metrics (Track in PostHog)
- Pricing page views (target: 500/month in 30 days)
- Upgrade clicks (target: 100/month in 30 days)
- Conversion rate (target: 2% in 30 days)
- Annual vs monthly ratio (target: 60% annual)
- Churn rate (target: <5% monthly)

---

## Quick Start Commands

### Local Development
```bash
cd ~/.openclaw/workspace/repos/MusicGen
npm run dev
# Navigate to http://localhost:3000/pricing
```

### Stripe Test
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
stripe trigger checkout.session.completed
```

---
**Timeline**: 1 week total
**Priority**: Critical for revenue growth
**Risk**: Low (existing infrastructure supports it)
