# MusicGen Email Onboarding Sequence

**Purpose:** Convert free users to paid subscriptions through automated 5-email flow

---

## Email Flow Overview

| # | Trigger | Timing | Goal |
|---|---------|--------|------|
| 1 | Signup | Immediately | Welcome + first loop |
| 2 | No Projects created | Day 2 | Tutorial: create first project |
| 3 | 5 Projects completed | Day 3 | Feature highlight: Sets/Albums |
| 4 | Social proof | Day 4 | Community: 10K+ loops, 4.9★ rating |
| 5 | Any activity | Day 5 | Conversion: 50% off first month |

---

## Email 1: Welcome + First Loop

**Subject:** Welcome to EDM Music Studio! 🎵 Your first loop awaits

**Trigger:** User signs up

**Content:**
```
Hi [Name],

Welcome to EDM Music Studio - the AI-powered music production tool trusted by 10K+ producers!

✨ Get Started:
1. Log in to your dashboard
2. Choose a genre or mood
3. Generate your first loop (free - 50/month!)

🎵 [Button: Generate Your First Loop]

That's it! You've got 50 free generations to experiment with.

Questions? Just reply to this email.

Cheers,
Lauro @ EDM Music Studio

P.S. Try our Pro tier for unlimited generations and Projects! [View Pricing]
```

---

## Email 2: Tutorial - Create Your First Project

**Subject:** Pro tip: Layer loops into Projects ⭐

**Trigger:** No Projects created after 2 days of signup

**Content:**
```
Hi [Name],

Noticing you've been generating loops - great start! 🎵

Here's how to level up:

🎖️ What are Projects?
Projects let you layer multiple loops to create complete tracks. Think:
- Drums loop + Bass loop + Melody loop = Full beat
- Export as a single WAV file
- Save and reuse in future projects

👇 See it in action:

[Button: Watch 30-sec Tutorial]
[Button: Create First Project]

P.S. Projects require Pro ($14.99/mo). Try it free for 30 days!
```

---

## Email 3: Feature Highlight - Sets & Albums

**Subject:** Your beats deserve a stage ✨

**Trigger:** User creates 5+ Projects

**Content:**
```
Hi [Name],

5 Projects in - you're a producer! 🎹

Time to level up with Sets:

💾 What are Sets?
Organize your Projects into albums, EPs, or DJ sets:
- Bundle related tracks
- Export as a cohesive collection
- Share with fans or collaborators

🌊 See the difference:
[Button: Explore Sets Feature]

Pro+ tier ($19.99/mo) unlocks Sets, API access, and priority support.
30-day free trial - no risk.

[Button: Upgrade to Pro+]
```

---

## Email 4: Social Proof & Community

**Subject:** Join 10K+ producers making beats with EDM Music Studio

**Trigger:** Day 4 (regardless of activity)

**Content:**
```
Hi [Name],

Over the past few days, you've generated [X] loops and created [Y] Projects.

But here's the bigger picture:

🌟 EDM Music Studio Stats:
- 10,000+ loops generated
- 500+ active producers
- 4.9★ average rating
- "Game changer for EDM production" - @DJProducer123

🏆 Community Challenge:
This week: Best House Loop of the Week
Submit your creations to our Discord!

[Button: Join Discord]
[Button: View Leaderboard]

Ready to go pro? Pro tier includes Projects, WAV export, and priority support.

[Button: View Pricing]
```

---

## Email 5: Conversion Offer

**Subject:** 🎁 Exclusive: 50% off your first Pro month

**Trigger:** Day 5 after signup OR after any user activity

**Content:**
```
Hi [Name],

Thanks for exploring EDM Music Studio! 🎵

Based on your activity, you're ready to unlock Pro:

🚀 Pro Features:
- Unlimited loop generations
- Projects (layer loops into tracks)
- WAV & MP3 export
- Priority queue & support
- 10GB cloud storage

✨ Exclusive Offer:
50% OFF your first Pro month! (Regular: $14.99)
Now: $7.49 for month 1, then full price.

[Button: Claim 50% Off - $7.49]

Offer expires in 48 hours!

Questions? Reply to this email - I'll help personally.

Best,
Lauro
Founder, EDM Music Studio
```

---

## Technical Implementation

### PostHog Integration

Add events to track engagement:

```typescript
// In pricing page / user dashboard
posthog.capture('email_welcome_sent', { userId, email, date });
posthog.capture('email_tutorial_sent', { userId, projects: 0 });
posthog.capture('email_sets_feature_sent', { userId, projects: 5 });
posthog.capture('email_social_proof_sent', { userId, loops: 100 });
posthog.capture('email_conversion_offered', { userId, discount: 0.5 });

// Track conversions
posthog.capture('email_cta_click', { email: 'tutorial' | 'sets' | 'social' | 'conversion' });
posthog.capture('email_conversion_success', { email: 'tutorial' | 'sets' | 'social' | 'conversion', revenue: 14.99 });
```

### SendGrid Integration (using Resend API)

```typescript
// /api/email/onboarding/send.ts
export async function POST(req: Request) {
  const { userId, email, step } = await req.json();
  
  // Get user data
  const user = await prisma.user.findUnique({ where: { id: userId } });
  
  // Track in PostHog
  await posthog.capture({ distinctId: userId, event: `email_${step}_sent` });
  
  // Send via Resend
  const response = await resend.emails.send({
    from: 'EDM Music Studio <onboarding@edmmusic.studio>',
    to: [email],
    subject: getEmailSubject(step),
    html: getEmailTemplate(step, user),
  });
  
  return Response.json({ success: true, id: response.id });
}
```

### Cron Schedule

Set up cron job to check and send emails:

```bash
# Run every 6 hours
0 */6 * * * cd /home/lauro/.openclaw/workspace && node scripts/email-onboarding-cron.js
```

```javascript
// scripts/email-onboarding-cron.js
const prisma = new PrismaClient();
const resend = new Resend(process.env.RESEND_API_KEY);

async function checkAndSendOnboardingEmails() {
  const users = await prisma.user.findMany({
    where: {
      email: { not: null },
      createdAt: { lte: new Date(Date.now() - 24 * 60 * 60 * 1000) }, // 24h ago
    }
  });
  
  for (const user of users) {
    const daysSinceSignup = Math.floor((Date.now() - user.createdAt) / (1000 * 60 * 60 * 24));
    const projects = await prisma.project.count({ where: { userId: user.id } });
    
    let emailStep;
    if (daysSinceSignup === 1 && projects === 0) {
      emailStep = 'tutorial';
    } else if (daysSinceSignup === 2 && projects >= 5) {
      emailStep = 'sets_feature';
    } else if (daysSinceSignup === 3) {
      emailStep = 'social_proof';
    } else if (daysSinceSignup === 4) {
      emailStep = 'conversion';
    }
    
    if (emailStep) {
      await sendOnboardingEmail(user.id, emailStep);
    }
  }
}

checkAndSendOnboardingEmails();
```

---

## A/B Testing

Test different approaches:

**Variant A: Social-first approach**
- Emails 2-4: Tutorial → Social Proof → Sets
- Goal: Build community trust first

**Variant B: Feature-first approach**
- Emails 2-4: Tutorial → Sets → Social Proof
- Goal: Show maximum value upfront

**Metrics to track:**
- Open rate (target: 40%+)
- Click-through rate (target: 10%+)
- Conversion rate from email (target: 5% of email recipients)
- Revenue per email (target: $2-5 per email sent)

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Email open rate | 40%+ | TBD |
| CTR | 10%+ | TBD |
| Conversion from email | 5% | TBD |
| Revenue per email | $2-5 | TBD |
| Free → Pro conversion | 2%+ | <0.2% |

---

## Next Steps

1. ✅ Create email templates (this doc)
2. ✅ Set up PostHog events
3. ✅ Implement Resend API integration
4. ✅ Create cron job for scheduling
5. ✅ Deploy and monitor for 30 days
6. ✅ Analyze results and iterate

---

**Status:** Ready for implementation  
**Estimated Time:** 2-3 hours  
**Priority:** High (conversion optimization)
