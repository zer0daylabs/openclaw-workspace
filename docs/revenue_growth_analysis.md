# Revenue Growth Analysis Plan

## Goal
Identify actionable opportunities to increase revenue for Zer0Day Labs by analyzing product usage, retention, and feature adoption using PostHog and internal metrics.

## Data Sources
1. **PostHog** (host: https://us.posthog.com)
   - Event stream: `signup`, `login`, `purchase`, `feature_use`, `session_start`, etc.
2. **Stripe** (subscription billing data) – available via Stripe API using the key stored in the password vault.
3. **Postgres databases** (MusicGen, AudioStudio) – can extract user counts, session logs.
4. **PostHog insights** – existing dashboards on user retention, funnel conversion, feature adoption.

## Analysis Steps
1. **Retention Analysis**
   - Create a *Retention* query in PostHog for the `signup` event.
   - Filter by `product` property (`MusicGen`, `AudioStudio`).
   - Export the retention data for 7, 14, and 30 days.
   - Identify the cohort that drops off most quickly.

2. **Feature Adoption**
   - Build a *Trend* insight for the `feature_use` event.
   - Filter by specific features (e.g., “Loop Generation”, “Project Creation”, “Set Export”).
   - Compare daily active users (DAU) vs. feature usage.
   - Highlight underused features for potential improvements or promotion.

3. **Funnel Analysis**
   - Funnel: `signup` → `login` → `first_loop_generation` → `purchase`.
   - Calculate drop‑off rates at each step.
   - Investigate where users are leaving the funnel.

4. **Cohort Analysis**
   - Group users by signup month.
   - Track revenue per cohort and compare growth.
   - Identify months with higher churn or lower upsell.

5. **Stripe Revenue & Churn**
   - Query Stripe API for MRR, churn rate, and customer lifetime value (CLV).
   - Correlate churn with events in PostHog (e.g., `cancel_subscription`).

6. **Product‑Level Summary**
   - Combine data to produce:
     * DAU, MAU, churn per product.
     * Revenue per product.
     * Feature adoption heat map.

## Deliverables
- **Report** in Markdown (`docs/revenue_growth_report.md`) with tables, charts, and insights.
- **Action Plan**: Prioritized list of high‑impact improvements (e.g., UX tweaks, feature releases, marketing campaigns).
- **Dashboard**: Update PostHog dashboards to visualize key metrics.

## Timeline
| Task | Owner | Due |
|------|-------|-----|
| Create PostHog queries | Analytics | 2026‑03‑15 |
| Pull Stripe data | Backend | 2026‑03‑15 |
| Generate report | Data Team | 2026‑03‑20 |
| Publish action plan | Product | 2026‑03‑22 |

---
**Note**: All API keys and secrets are stored in the local vault. Ensure that the vault is mounted when running scripts.
