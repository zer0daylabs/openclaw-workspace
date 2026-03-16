# Stripe — CB Knowledge Summary

Last updated: 2026-03-15
Proficiency: basic
Source: MusicGen/AudioStudio integration, credentials file

## What It Is
Payment processing platform. Handles subscriptions, one-time payments, invoicing, and billing.

## Our Use Case
- MusicGen and AudioStudio use Stripe for subscriptions
- Current MRR: $9.99 (1 active subscription)
- Default to test mode — ask Lauro before touching live
- Available balance: ~$28 USD

## Key Concepts
- **Customers** — Users with payment methods
- **Subscriptions** — Recurring billing (what our MRR comes from)
- **Products + Prices** — Define what you sell and at what price
- **Webhooks** — Stripe notifies your app of events (payment succeeded, subscription canceled, etc.)
- **Payment Intents** — Represent a payment attempt
- **Checkout Sessions** — Pre-built payment pages

## Configuration
- Credentials: `~/.openclaw/workspace/.credentials/stripe.json`
- Financial tracking: `FINANCES.md` + `scripts/financial-report.sh`
- Webhook endpoint: configured in Stripe dashboard, points to Vercel API route

## Key API Patterns
```bash
# List subscriptions (test mode)
curl https://api.stripe.com/v1/subscriptions -u sk_test_xxx:

# List customers
curl https://api.stripe.com/v1/customers -u sk_test_xxx:

# Get balance
curl https://api.stripe.com/v1/balance -u sk_test_xxx:
```

## Gotchas
- Test mode vs live mode: different API keys, different data
- Webhook signatures must be verified (STRIPE_WEBHOOK_SECRET env var)
- Subscription lifecycle: trial → active → past_due → canceled
- Always use idempotency keys for payment creation
- Price IDs are immutable — create new price, archive old one

## Resources
- Docs: https://stripe.com/docs
- API Reference: https://stripe.com/docs/api
- Webhooks: https://stripe.com/docs/webhooks
- Testing: https://stripe.com/docs/testing
