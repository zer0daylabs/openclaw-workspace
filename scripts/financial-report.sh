#!/bin/bash

# Financial Report Generator for Zer0Day Labs
# Updates FINANCES.md with current revenue/costs

echo "=== ZER0DAY LABS FINANCIAL REPORT ==="
echo "Generated: $(date '+%Y-%m-%d %H:%M %Z')"
echo ""

# Get Stripe data
LIVE_KEY=$(jq -r '.live.secretKey' ~/.openclaw/workspace/.credentials/stripe.json)

echo "📊 STRIPE REVENUE"
echo "=================="

# Balance
BALANCE=$(curl -s -u "$LIVE_KEY": "https://api.stripe.com/v1/balance" | \
  jq -r '"$" + (.available[0].amount/100|tostring)')
echo "Available Balance: $BALANCE"

# Active subscriptions (MRR)
MRR=$(curl -s -u "$LIVE_KEY": "https://api.stripe.com/v1/subscriptions?status=active" | \
  jq -r '[.data[].items.data[0].price.unit_amount] | add/100' | \
  awk '{printf "%.2f", $1}')
echo "Monthly Recurring Revenue: \$$MRR"

# Recent charges
echo ""
echo "Recent Charges (Last 5):"
curl -s -u "$LIVE_KEY": "https://api.stripe.com/v1/charges?limit=5" | \
  jq -r '.data[] | (.created | strftime("%Y-%m-%d")) + " | $" + (.amount/100|tostring) + " | " + .description'

echo ""
echo "💸 ESTIMATED MONTHLY COSTS"
echo "=========================="
echo "CB (AI Usage): ~\$1-2"
echo "Vercel: TBD"
echo "Other Infrastructure: TBD"
echo ""
echo "📈 NET ESTIMATE: \$$MRR - \$X = \$Y"