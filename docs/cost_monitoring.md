# Cost Monitoring Dashboard

This dashboard tracks infrastructure costs vs revenue for Zer0Day Labs products.

## Current Cost Structure (as of 2026-03-09)

### Railway
- **Account**: support@zer0daylabs.com
- **Available Balance**: $37.28
- **Monthly Recurring Revenue**: $9.99 (consistent since Nov 2025)
- **Active Projects**: 7 total
  - `audio-converter` - Keep (functional)
  - `user-data-subscriptions` - Keep (functional)
  - `new-db-app` - Needs rename to AudioStudio-DB
  - `lucky-playfulness` - Needs rename to MusicGen-DB
  - `SlackBot` - Keep (functional, 2 services)
  - `truthful-warmth` - DELETE (unused DB)
  - `appealing-laughter` - DELETE (unused DB)

### Vercel
- **Accounts**: support-9645
- **Projects**: MusicGen (edmmusic.studio), AudioStudio (audiostudio.ai)
- **Costs**: TBD (requires dashboard access or API query)

### Stripe
- **MRR**: $9.99
- **Customers**: 1-2 subscribers (based on MRR)
- **Growth Opportunity**: High - limited subscriber base

## Cost Monitoring Script

Use the script at `scripts/cost_monitor.py` to automate cost tracking:

```bash
# Run cost monitoring
python3 scripts/cost_monitor.py

# Set up cron for hourly checks
# 0 * * * * cd ~/.openclaw/workspace && python3 scripts/cost_monitor.py >> logs/cost_monitor.log
```

## Key Metrics to Track

1. **Infrastructure Costs**
   - Railway: Balance depletion rate, project usage
   - Vercel: Bandwidth, function invocations, deployments
   - Database: Postgres storage and I/O costs

2. **Revenue**
   - Stripe: MRR, customer count, churn rate
   - Conversion rate: Free → Paid
   - LTV: Customer lifetime value

3. **Profitability**
   - Gross margin: Revenue - Infrastructure costs
   - CAC: Customer acquisition cost (if applicable)
   - Burn rate: Monthly spend vs revenue

## Alerts

Set up alerts for:
- Balance below $10 → Alert Lauro to add funds
- Infra costs > 50% of MRR → Investigate optimization
- Revenue growth < 5% monthly → Review growth strategy

## Optimization Opportunities

1. **Immediate**: Delete unused Railway DBs (truthful-warmth, appealing-laughter)
2. **Short-term**: Connect Vercel to Railway databases for cost consolidation
3. **Long-term**: Scale infrastructure as user base grows

---
**Status**: Dashboard framework created. Implementation pending Vercel API access.
