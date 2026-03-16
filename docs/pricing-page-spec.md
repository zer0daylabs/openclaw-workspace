# MusicGen Pricing Page Specification

## Overview
This document specifies the 3-tier pricing structure for MusicGen (edmmusic.studio) to drive user conversion from free to paid plans.

---

## Pricing Tiers

### 🥉 **Free Tier** ($0/month)
**Target**: Casual EDM enthusiasts testing the product

**Features Included**:
- ✅ Up to 50 loop generations per month
- ✅ Access to basic loop types (drums, bass, synth)
- ✅ Basic BPM/key controls
- ✅ Individual loop downloads (MP3 format)
- ✅ Access to public loops library
- ✅ Community support (Discord forum)

**Limitations** (gated behind upgrade):
- ❌ No Projects feature (layering loops)
- ❌ No Sets feature (albums/EPs)
- ❌ WAV/FLAC export formats
- ❌ Priority support
- ❌ API access

---

### 🥈 **Pro Tier** ($9.99/month or $99/year - 2 months free)
**Target**: Music producers and hobbyists

**Features Included** (all Free features +):
- ✅ Unlimited loop generations
- ✅ All loop types (drums, bass, synth, vocals, etc.)
- ✅ Advanced BPM/key controls
- ✅ Projects feature (layer multiple loops)
- ✅ WAV and MP3 export formats
- ✅ Priority email support
- ✅ 10GB cloud storage for projects

**Limitations** (gated behind Pro+ upgrade):
- ❌ No Sets feature (full album creation)
- ❌ FLAC export format
- ❌ API access
- ❌ Custom sample packs

---

### 🥇 **Pro+ Tier** ($19.99/month or $199/year - 2 months free)
**Target**: Professional music producers and studios

**Features Included** (all Pro features +):
- ✅ Unlimited loop generations
- ✅ All loop types + custom sample packs
- ✅ Full BPM/key control suite
- ✅ Projects feature (unlimited projects)
- ✅ Sets feature (albums, EPs, DJ sets)
- ✅ All export formats (WAV, MP3, FLAC)
- ✅ Priority support (24hr response)
- ✅ 100GB cloud storage
- ✅ API access for batch generation
- ✅ Early access to new features
- ✅ Custom sample pack creation
- ✅ Collaborative workspaces (up to 3 users)

---

## Conversion Strategy

### **Free → Pro Conversion Triggers**

1. **After 10 free generations**: Show "Upgrade to Pro" CTA
2. **When accessing Projects**: Show "Projects require Pro tier" message with upgrade CTA
3. **After creating 5 Projects**: Show "Upgrade to Pro+ for Sets" message

### **Yearly Billing Incentive**
- Annual billing = 2 months free (17% discount)
- Display savings: "Save $20/year with annual billing"
- Default to annual option with toggle for monthly

---

## Pricing Page Layout

```
[HERO SECTION]
🎵 Create Amazing EDM Music
"AI-Powered Music Production"
[Sign Up Free - 30 Day Trial] [View Pricing]

[PRICING CARDS - 3 columns]
┌─────────────┬──────────────┬──────────────┐
│   FREE      │     PRO      │     PRO+     │
│    $0       │   $9.99/mo   │   $19.99/mo  │
│             │  (or $99/yr) │  (or $199/yr)│
├─────────────┼──────────────┼──────────────┤
│   50/month  │  Unlimited   │  Unlimited   │
│   Basic     │  All Loops   │  All +Custom │
│   MP3 only  │  Projects    │  Sets/Albums │
│   Community │   Email supp │   Priority   │
│             │   10GB       │   API/Custom │
├─────────────┼──────────────┼──────────────┤
│ [Start Free]│ [Choose Pro]│ [Choose Pro+]│
└─────────────┴──────────────┴──────────────┘
[Toggle: Monthly | Annual (-17%)]

[COMPARISON TABLE]
Feature | Free | Pro | Pro+
--------|------|-----|-----
Loops   | 50/m | Unlimited | Unlimited
Projects| ❌   | ✅        | ✅
Sets    | ❌   | ❌        | ✅
Formats | MP3  | MP3/WAV   | All
Support | Comm | Email     | Priority

[FAQ SECTION]
- What's the difference between Free and Pro?
- Can I cancel anytime?
- Is there a student discount?
- How does billing work?

[CTA FOOTER]
🚀 Start your 30-day free trial
No credit card required
Cancel anytime
```

---

## Implementation Notes

### Technical Requirements
- Stripe subscription integration
- Feature flagging system (to enable/disable features by tier)
- Email capture at signup (for onboarding)
- PostHog analytics on pricing page (conversion tracking)

### Migration Path
1. Current free users → remain on Free tier (grandfathered)
2. New users → see pricing page at signup
3. Free users who exceed 50 loops/month → prompt to upgrade

---

## Success Metrics
- **Pricing page conversion rate**: Target 2% in first 30 days
- **Free→Pro conversion**: Track via PostHog funnel
- **Annual vs Monthly ratio**: Target 60% annual (recurring revenue)
- **Churn rate**: Keep <5% monthly

---
**Next Steps**:
1. Implement pricing page UI (React/Next.js)
2. Set up Stripe billing for Pro/Pro+ tiers
3. Implement feature gating logic
4. Add PostHog conversion tracking
5. Launch and monitor metrics
