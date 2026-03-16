# Zer0Day Labs Infrastructure Cost Analysis

## Current Infrastructure (2026-03-09)

### Railway Projects (7 total)
| Project | Type | Status | Purpose | Action |
|--|--|--|--|--|
| lucky-playfulness | PostgreSQL DB | Active | MusicGen DB | Rename to `MusicGen-DB` |
| truthful-warmth | PostgreSQL DB | **Unused** | ? | **Delete** (2025-10-20) |
| appealing-laughter | PostgreSQL DB | **Unused** | ? | **Delete** (2025-10-13) |
| audio-converter | App + DB | Active | Audio audio converter | Keep |
| user-data-subscriptions | PostgreSQL DB | Active | User data | Keep |
| new-db-app | PostgreSQL DB | Active | ? | Rename to `AudioStudio-DB` |
| SlackBot | App + DB | Active | Teambot | Keep |

### Estimated Costs
- **Railway**: ~$5-10/mo (5 active projects, 2 unused)
- **Vercel**: ~$0-20/mo (2 Next.js projects, likely on Hobby plan)
- **Stripe**: 2.9% + $0.30 per transaction (revenue share)
- **PostHog**: Likely free tier (~$0-20/mo)
- **Sentry**: ~$0-50/mo (depending on usage)
- **Total Monthly**: ~$10-100 (highly variable based on usage)

## Cost Optimization Opportunities

### 🎯 Immediate Savings (Week 1)

#### 1. **Delete Unused Railway DBs** (Priority: Critical)
**Savings**: ~$2-4/month
- `truthful-warmth` (created 2025-10-20) - unused
- `appealing-laughter` (created 2025-10-13) - unused

**Action**:
1. Log in to Railway dashboard
2. Delete these two projects
3. Verify balance increases by ~$2-4

#### 2. **Enable Yearly Billing for Railway**
**Savings**: 10-20% on Railway infrastructure
- Railway offers discounts for yearly commitments
- Reduces MRR variability

### 📈 Medium-Term Optimizations (Month 1)

#### 3. **Vercel Cost Optimization**
**Potential Savings**: $5-15/month
- Review Vercel usage (bandwidth, serverless function duration)
- Consider migrating to Pro plan if at scale
- Enable caching to reduce bandwidth costs

#### 4. **PostHog/Sentry Plan Review**
**Potential Savings**: $20-50/month
- Check current plan levels
- Downgrade unused features
- Consider self-hosting for advanced analytics

### 💡 Long-Term Strategy (Quarter)

#### 5. **Infrastructure Monitoring Dashboard**
**Goal**: Track infrastructure costs vs revenue
- Add cost tracking to dashboard
- Alert when costs exceed X% of revenue
- Optimize based on usage patterns

## Cost/Revenue Ratio

| Metric | Value | Target |
|--|--|--|
| Monthly Revenue | $9.99 | $200+ (90 days) |
| Estimated Infrastructure | $10-50 | <$20 |
| Cost/Revenue Ratio | >100% | <10% |
| Net Margin | Negative | +85%+ |

### Key Insight: **Cost Optimization is Urgent**

Current infrastructure costs likely exceed revenue. With the growth plan targeting $200 MRR:
- **Break-even point**: At $200 MRR, infrastructure should be <$20/mo (10% ratio)
- **Current state**: Costs probably ~100-500% of revenue
- **Action needed**: Immediate cleanup + ongoing monitoring

## Action Items

### Week 1 (Immediate)
- [ ] Delete unused Railway DBs (`truthful-warmth`, `appealing-laughter`)
- [ ] Enable yearly billing for Railway
- [ ] Review Vercel usage and bandwidth

### Week 2-4
- [ ] Set up cost monitoring dashboard
- [ ] Review PostHog/Sentry usage
- [ ] Implement usage-based cost alerts

### Month 2
- [ ] Optimize based on usage patterns
- [ ] Consider cost-effective alternatives (e.g., self-hosted PostHog)
- [ ] Review infrastructure quarterly

## Monitoring Tools

### Recommended Dashboard
- **Google Sheets**: Track monthly costs and revenue
- **Vercel Dashboard**: Monitor bandwidth, function duration
- **Railway Dashboard**: Monitor project usage
- **Stripe Dashboard**: Track revenue, churn, MRR
- **PostHog**: User analytics (already in place)

---
**Conclusion**: Immediate cost savings from deleting unused Railway projects can reduce monthly burn by 20-40%. Combined with growth plan execution, the business should move from negative to positive margins within 3 months.
