# Freqtrade Strategy Metrics — RsiMacD on Kraken (Dry Run)

**Started:** 2026-03-09 ~12:20 AM MST
**Strategy:** RsiMacD — RSI(14) crossover (buy < 30, sell > 70) + MACD histogram
**Timeframe:** 5m | **Exchange:** Kraken | **Stake:** $10 USDT/trade | **Wallet:** $10K simulated
**Pairs:** 20 (BTC, ETH, SOL, ADA, DOT, AVAX, LINK, ATOM, XRP, DOGE, SHIB, LTC, APE, BNB, BCH, ALGO, TON, XMR, MANA, XTZ)

---

## Observations Log

### 2026-03-09 — Night 1 (First trades)

**10:19 PM MST** — Bot running with original 3 pairs (BTC, ETH, SOL). All RSI mid-range (43-50). No trades yet. MACD histograms slightly negative (mild bearish momentum).

| Pair | Price | RSI | MACD_H |
|---|---|---|---|
| BTC/USDT | $67,136 | 48.9 | -120.92 |
| ETH/USDT | $1,980 | 54.0 | -1.59 |
| SOL/USDT | $83.33 | 50.9 | -0.11 |

**11:59 PM MST** — RSI dropping across the board. SOL approaching buy zone.

| Pair | Price | RSI | MACD_H |
|---|---|---|---|
| BTC/USDT | $67,315 | 43.0 | -93.22 |
| ETH/USDT | $1,986 | 42.4 | -6.16 |
| SOL/USDT | $83.13 | 37.4 | -0.24 |

**~12:20 AM MST** — **First 2 trades triggered!** RSI dipped below 30 and crossed back up.
- Trade #1: **ETH/USDT** entry $1,967.80
- Trade #2: **SOL/USDT** entry $82.57

**12:35 AM MST** — Expanded to 20 pairs. Bot restarted. Both trades survived restart.

**1:33 AM MST** — Both trades green. New pairs showing interesting RSI extremes.

| Metric | Value |
|---|---|
| ETH/USDT | entry $1,967.80 → $1,999.79 (+1.62%) |
| SOL/USDT | entry $82.57 → $83.83 (+1.53%) |

**Missed entries detected:**
- **SHIB/USDT** RSI 19.9 — deeply oversold but bot didn't enter (possible gap: RSI jumped from <30 to >30 between candle closes)
- **MANA/USDT** RSI 13.0 — extremely oversold, same issue

**3:09 AM MST** — 2 new trades opened from expanded watchlist. MANA bounced from 13→90 without being caught.

| Trade | Pair | Entry | Current | P&L |
|---|---|---|---|---|
| #1 | ETH/USDT | $1,967.80 | $2,004.42 | +1.86% (unfilled) |
| #2 | SOL/USDT | $82.57 | $84.06 | +1.80% (unfilled) |
| #3 | ATOM/USDT | $1.7297 | $1.7432 | +0.78% (unfilled) |
| #4 | DOT/USDT | $1.4798 | $1.4820 | -0.82% (filled) |

**3:56 AM MST** — P&L bug investigated and fixed
- **Root cause:** Limit buy orders at bid price never fill in dry_run when price bounces up (which is exactly what RSI<30 signals produce)
- Trades #1-3 had `amount=0`, `filled=0` — ghost trades
- **Fix:** Changed `order_types.entry` from `limit` → `market`, `price_side` from `bid` → `other`
- Deleted stuck trades #1-3, restarted bot
- New trade #10 XMR/USDT immediately filled correctly: entry $343.20, P&L +0.13%

**7:46 AM MST** — Morning check-in. Market order fix working perfectly. 7 total trades, 6 closed.

| # | Pair | Entry | Exit | P&L | Result | Reason |
|---|---|---|---|---|---|---|
| #4 | DOT/USDT | $1.4798 | $1.4929 | +0.23% | ✅ Win | exit_signal |
| #5 | AVAX/USDT | $9.02 | $9.15 | +0.63% | ✅ Win | exit_signal |
| #6 | LTC/USDT | $53.07 | $53.89 | +0.72% | ✅ Win | exit_signal |
| #7 | BNB/USDT | $625.46 | $629.22 | -0.20% | ❌ Loss | exit_signal |
| #8 | XTZ/USDT | $0.3648 | $0.3673 | -0.12% | ❌ Loss | exit_signal |
| #9 | ALGO/USDT | $0.0827 | $0.0839 | +0.59% | ✅ Win | exit_signal |
| #10 | XMR/USDT | $343.20 | — | +0.64% | 🟢 Open | — |

**Summary:** Win rate 67% (4/6), closed profit +$0.187 USDT, best pair LTC/USDT (+0.72%)

RSI anomalies:
- TON/USDT RSI 100.0, SHIB/USDT RSI 99.8 — pinned at max, likely low-liquidity or stale data
- MANA/USDT RSI 90.3 — still pinned high since 1:33 AM (6+ hours)
- APE/USDT RSI normalized from 99.9 → 45.1

**11:01 AM MST** — Market softening, 5 open trades all red. Total P&L flipped negative.

| # | Pair | Entry | Current | P&L | Notes |
|---|---|---|---|---|---|
| #10 | XMR/USDT | $343.20 | $342.03 | -1.14% | Was +0.64% at 7:46 AM |
| #11 | BCH/USDT | $446.95 | $449.85 | -0.15% | Recovering from -0.99% |
| #12 | ALGO/USDT | $0.0836 | $0.0832 | -1.28% | 2nd ALGO trade |
| #13 | ATOM/USDT | $1.7487 | $1.7447 | -1.02% | New since 9:23 AM |
| #14 | MANA/USDT | $0.0904 | $0.0903 | -0.90% | New — entered after RSI crashed from 90→0.3 |

**Summary:** Closed P&L still +$0.187, but total P&L now **-$0.264** from open drawdown. BTC drifting $69K→$68.6K.

RSI anomaly updates:
- **TON/USDT** — un-pinned from 100→51.6 ✅ data flowing again
- **MANA/USDT** — crashed from 90.3→0.3 (triggered buy #14) — extreme swing confirms thin liquidity
- **APE/USDT** — re-pinned at 100.0 (was 45.1 at 9:23 AM) — data artifact confirmed
- **XTZ/USDT** — RSI 31.1, near buy zone

**12:20 PM MST** — Open positions recovering. 2 new entries (#15 BNB, #16 XTZ). Total P&L improving.

| # | Pair | Entry | Current | P&L | Δ from 11 AM |
|---|---|---|---|---|---|
| #10 | XMR/USDT | $343.20 | $345.37 | -0.17% | ↑ from -1.14% |
| #11 | BCH/USDT | $446.95 | $450.49 | -0.01% | ↑ from -0.15% |
| #12 | ALGO/USDT | $0.0836 | $0.0835 | -0.92% | ↑ from -1.28% |
| #13 | ATOM/USDT | $1.7487 | $1.7528 | -0.56% | ↑ from -1.02% |
| #14 | MANA/USDT | $0.0904 | $0.0908 | -0.31% | ↑ from -0.90% |
| #15 | BNB/USDT | $636.57 | $636.89 | -0.75% | 🆕 New |
| #16 | XTZ/USDT | $0.3655 | $0.3654 | -0.82% | 🆕 New |

**Summary:** 13 total trades, 6 closed, 7 open. Total P&L **-$0.169** (improving from -$0.264). All 5 earlier positions recovered. BCH nearly breakeven.

RSI notes:
- BCH/USDT RSI 27.2 🔥 — below buy threshold while already in open trade
- MANA RSI still pinned at 0.3 — stale data confirmed
- SHIB RSI 74.0 — stuck at this level for 10+ hours

**4:02 PM MST** — Broad market selloff. Bot loaded up to 14 open trades, all red. 5 more trades closed since 12:20 PM.

New closed trades:

| # | Pair | Entry | Exit | P&L | Result |
|---|---|---|---|---|---|
| #11 | BCH/USDT | $446.95 | $451.09 | +0.12% | ✅ Win |
| #12 | ALGO/USDT | $0.0836 | $0.0843 | +0.01% | ✅ Win (barely) |
| #13 | ATOM/USDT | $1.7487 | $1.7641 | +0.08% | ✅ Win |
| #15 | BNB/USDT | $636.57 | $639.06 | -0.41% | ❌ Loss |
| #16 | XTZ/USDT | $0.3655 | $0.3673 | -0.31% | ❌ Loss |

14 open trades (all red, -0.68% to -1.76%):

| # | Pair | Entry | Current | P&L |
|---|---|---|---|---|
| #10 | XMR | $343.20 | $340.15 | -1.68% |
| #14 | MANA | $0.0904 | $0.0903 | -0.93% |
| #17 | XTZ | $0.3645 | $0.3620 | -1.48% |
| #18 | TON | $1.342 | $1.329 | -1.76% |
| #19 | BCH | $449.21 | $446.68 | -1.36% |
| #20 | APE | $0.0947 | $0.0938 | -1.74% |
| #21 | ETH | $2,010.93 | $2,001.51 | -1.26% |
| #22 | DOT | $1.4915 | $1.4881 | -1.02% |
| #23 | AVAX | $9.29 | $9.26 | -1.12% |
| #24 | LINK | $8.9209 | $8.8975 | -1.06% |
| #25 | SHIB | $5.44e-6 | $5.42e-6 | -1.16% |
| #26 | LTC | $53.89 | $53.68 | -1.17% |
| #27 | ALGO | $0.0834 | $0.0831 | -1.13% |
| #28 | ADA | $0.2548 | $0.2552 | -0.68% |

**Summary:** 25 total trades, 11 closed (7W/4L = 64%), 14 open all red. Closed P&L +$0.136. **Total P&L -$1.624.** 11 of 20 pairs below RSI 30 — market-wide dip. Bot buying into a downtrend — classic mean-reversion trap. No stoploss hits yet (worst -1.76%).

**Critical insight:** RSI mean-reversion without a trend filter buys every dip in a selloff. Need a higher-timeframe trend guard (e.g., 1h EMA slope > 0 required for entry).

**7:11 PM MST** — Evening check. Selloff positions unwinding. 6 more closed since 4 PM, 1 new trade opened.

Newly closed:

| # | Pair | Entry | Exit | P&L | Result |
|---|---|---|---|---|---|
| #17 | XTZ/USDT | $0.3645 | $0.3643 | -0.85% | ❌ Loss |
| #19 | BCH/USDT | $449.21 | $448.39 | -0.98% | ❌ Loss |
| #22 | DOT/USDT | $1.4915 | $1.5048 | +0.09% | ✅ Win |
| #26 | LTC/USDT | $53.89 | $54.16 | -0.29% | ❌ Loss |
| #27 | ALGO/USDT | $0.0834 | $0.0838 | -0.33% | ❌ Loss |
| #28 | ADA/USDT | $0.2548 | $0.2580 | +0.45% | ✅ Win |
| #29 | BNB/USDT | $638.01 | $638.31 | -0.75% | ❌ Loss (new trade, opened & closed) |

8 open trades remaining (recovering):

| # | Pair | Entry | Current | P&L | Δ from 4 PM |
|---|---|---|---|---|---|
| #10 | XMR | $343.20 | $341.89 | -1.18% | ↑ from -1.68% |
| #14 | MANA | $0.0904 | $0.0910 | -0.11% | ↑ from -0.93% |
| #18 | TON | $1.342 | $1.329 | -1.76% | → same |
| #20 | APE | $0.0947 | $0.0937 | -1.84% | ↓ from -1.74% |
| #21 | ETH | $2,010.93 | $2,018.85 | -0.41% | ↑ from -1.26% |
| #23 | AVAX | $9.29 | $9.33 | -0.37% | ↑ from -1.12% |
| #24 | LINK | $8.9209 | $8.9188 | -0.82% | ↑ from -1.06% |
| #25 | SHIB | $5.44e-6 | $5.45e-6 | -0.61% | ↑ from -1.16% |

**End-of-day summary:** 26 total trades, 18 closed (9W/9L = 50%), 8 open all red. Closed P&L **-$0.132**. Total P&L **-$0.844**. Market bounced from afternoon lows (BTC $68.6K→$69.1K). Most open positions recovering.

---

## Day 1 Lessons Learned (2026-03-09)

### What Worked

1. **RSI crossover entry logic is sound** — In ranging/sideways markets (midnight–noon), the strategy correctly caught oversold bounces. The first 6 closed trades went 4W/2L = 67%, with losses capped small (-0.12% to -0.20%).

2. **Exit signals are reliable** — All 18 closed trades exited via `exit_signal` (RSI > 70), zero stoploss hits. The strategy doesn't hold losers — it exits when RSI recovers, even if the trade is underwater. Max loss was -0.98%.

3. **Market orders fix was correct** — Switching from limit to market orders for dry_run was essential. Every trade after the fix filled and tracked P&L correctly.

4. **Position recovery is real** — Multiple trades (DOT #4, BCH #11, ADA #28) entered red, dipped further, then recovered to close green. The wide stoploss (-10%) gives room for crypto volatility.

### What Didn't Work

1. **No trend filter = buying into selloffs** — The #1 lesson. At 4 PM, 11 of 20 pairs had RSI < 30 simultaneously. The bot opened 14 positions, all underwater. RSI mean-reversion works in ranging markets but catches falling knives in downtrends. This turned the day from profitable to negative.

2. **Low-liquidity pairs produce garbage RSI** — MANA (RSI 90→0.3→0.3 stuck), APE (RSI 4.5→100→4.5 cycling), TON (RSI 100→51→8.7) all showed erratic or stale RSI data. MANA has been at RSI 0.3 for 8+ hours. These pairs don't have enough volume on Kraken USDT markets for reliable 5m candles.

3. **Too many pairs = too much exposure** — With 20 pairs and max_open_trades=20, the bot can deploy $200 during a broad selloff. When all entries correlate (crypto sells off together), diversification is an illusion.

4. **Wins are too small** — Average win: +0.31%. Average loss: -0.50%. The risk/reward ratio is inverted. The strategy exits at RSI 70 crossover, but sometimes RSI hits 70 before the trade has moved enough to be profitable. Need either larger wins (trailing stop) or more selective entries.

### By The Numbers

| Metric | Value |
|---|---|
| Total trades | 26 (18 closed, 8 open) |
| Win rate | 50% (9W/9L) |
| Avg win | +0.31% |
| Avg loss | -0.50% |
| Best trade | LTC #6 +0.72% |
| Worst trade | BCH #19 -0.98% |
| Closed P&L | -$0.132 USDT |
| Total P&L | -$0.844 USDT |
| Max simultaneous open | 14 trades |
| Stoploss hits | 0 |
| Best pair | AVAX/USDT (won both trades) |
| Worst pair | BNB/USDT (lost all 3 trades) |

### Priority Improvements for Day 2

1. **🚨 Trend filter (CRITICAL)** — Add 1h EMA(50) slope check. Only allow entries when the higher timeframe trend is flat or up. This alone would have prevented the 14-trade selloff pile-up.

2. **🚨 Reduce pair count** — Remove APE, MANA, TON (stale RSI data). Consider removing SHIB too. Drop from 20 to 16 pairs. Reduce max_open_trades to 10 to limit correlated exposure.

3. **Add trailing stop** — e.g., trailing_stop=True, trailing_stop_positive=0.02, trailing_stop_positive_offset=0.03. This would lock in profits on runners instead of waiting for RSI 70.

4. **MACD confirmation** — Require MACD histogram turning positive before entry. Currently the strategy computes MACD but only uses RSI for signals. Adding MACD confirmation would filter out entries where momentum is still bearish.

5. **Tighten minimal_roi** — Current 5%@0m is never hit on $10 trades. Consider 2%@0m, 1%@30m, 0.5%@60m for faster profit-taking on small moves.

---

## Key Findings

### 1. RSI < 30 Crossover Works for Entry
- ETH and SOL both entered at RSI bounce from <30, immediately went green
- Strategy correctly identifies oversold bounces

### 2. 5m Timeframe May Miss Rapid Bounces
- SHIB went from RSI 19.9 → 62.6 without triggering entry
- MANA went from RSI 13.0 → 90.3 without triggering entry
- **Hypothesis:** RSI crossed above 30 within the same candle (open < 30, close > 30) — the strategy checks close values, so it saw the crossover but may not have had the previous candle below 30 to trigger the cross-above condition
- **Potential fix:** Consider using `crossed_above()` with a wider lookback, or add a 15m timeframe confirmation

### 3. Exit Signals Working Correctly
- All 18 closed trades exited via `exit_signal` (RSI > 70 crossover) — zero stoploss hits
- Losses are small (-0.12% to -0.98%) — strategy cuts losers via RSI recovery
- Winners modest (0.01% to 0.72%), losses often larger than wins — risk/reward inverted
- Final win rate: 9/18 = 50%

### 4. DOT Recovered
- Previously entered at -0.35%, closed at +0.23% — the "dead cat bounce" concern was unfounded
- Strategy's patience paid off

### 5. RSI Pinning on Low-Liquidity Pairs
- TON/USDT stuck at RSI 100.0, SHIB/USDT at 99.8, MANA at 90.3 for 6+ hours
- Likely thin order books causing price staleness on Kraken USDT pairs
- **Update (11 AM):** TON un-pinned (100→51.6), but MANA swung 90→0.3 and APE re-pinned at 100
- MANA's extreme RSI swing (90→0.3) triggered a buy entry (#14) — dangerous on illiquid pairs
- **Consider:** Remove APE, MANA from whitelist — erratic RSI from stale data produces false signals
- **Consider:** Add minimum volume filter to strategy to auto-skip thin pairs

### 7. Mean-Reversion Trap in Selloffs (4:02 PM)
- Broad market selloff: 11 of 20 pairs below RSI 30 simultaneously
- Bot opened 14 positions buying every dip — all underwater (-0.68% to -1.76%)
- RSI < 30 is a valid signal in ranging markets, but in a trending selloff it's a trap
- **Critical need:** Trend filter — e.g., require 1h EMA(50) slope > 0 before allowing entries
- Without trend context, the strategy keeps catching falling knives
- $140 deployed across 14 trades, total drawdown -$1.62

### 6. P&L Bug — RESOLVED
- **Root cause:** Limit orders (`entry: "limit"` + `price_side: "bid"`) never filled in dry_run. The price bounced up immediately after signal (expected for oversold bounces), so the simulator never matched the limit price.
- Trades #1-3 (ETH, SOL, ATOM) all had `amount=0`, `filled=0`, `status=open` — orders placed but never executed
- Trade #4 (DOT) filled because the price continued down after entry, hitting the limit
- **Fix applied (3:56 AM):** Changed to `order_types.entry: "market"` and `price_side: "other"`. Market orders fill instantly in dry_run.
- **Result:** New trade #10 (XMR/USDT) filled correctly with `amount=0.029`, P&L calculating at +0.13%
- Deleted stuck trades #1-3 via API, DOT #4 cleaned up on restart

---

## Strategy Parameters (Current — v8 Hyperopt-Optimized)

**Deployed:** 2026-03-11 ~7:22 PM MST

### Entry: EMA Crossover + Tunable Filters
| # | Condition | Value | Notes |
|---|---|---|---|
| 1 | EMA(9) crossed above EMA(21) | — | Bullish momentum crossover |
| 2 | ADX(14) > threshold | **22** | Trend must be present |
| 3 | RSI(14) < max | **54** | Not overbought — still has room to run |
| 4 | Volume > avg × multiplier | **0.6×** | Loose volume filter |
| 5 | 1h EMA(50) slope >= 0 | Required | Higher TF trend alignment |
| tag | `ema_cross` | — | Tracked via enter_tag |

### Exit Logic
| Exit | Condition | Notes |
|---|---|---|
| profit_protect | profit > **0.4%** + open > 15min | **Primary exit** — takes small consistent profits |
| force_exit | profit < 0 + open > **4h** | Cuts stale losers |
| ROI | 13.3%@0m, 4.4%@19m, 3.1%@37m, 0%@115m | Wide — rarely triggers, break-even at 2h |
| trailing_stop | 11.1% trail after 16.7% profit | Wide — rarely triggers |
| stoploss | **-28.8%** | Wide — emergency only |
| exit_signal | None | Disabled — every indicator-based exit tested was #1 source of losses |

### Other Parameters
| Parameter | Value |
|---|---|
| timeframe | 5m |
| informative_timeframe | 1h |
| pairs | 11 (ADA, ALGO, ATOM, AVAX, BCH, DOGE, DOT, LINK, LTC, XMR, XRP) |
| max_open_trades | 10 |
| startup_candle_count | 50 |
| param source | RsiMacD.json (hyperopt output, auto-loaded) |

---

## 30-Day Backtest Results (Feb 10 — Mar 12, 2026)

### Market Context
**Average market change: -1.5% across 15 pairs (10 losers, 5 winners)**

| Pair | 30-Day Change | | Pair | 30-Day Change |
|---|---|---|---|---|
| BCH/USDT | -13.9% | | LTC/USDT | +0.8% |
| ALGO/USDT | -10.0% | | LINK/USDT | +1.8% |
| SHIB/USDT | -6.1% | | XMR/USDT | +4.5% |
| ATOM/USDT | -5.9% | | AVAX/USDT | +5.4% |
| XRP/USDT | -3.7% | | DOT/USDT | +14.9% |
| DOGE/USDT | -3.6% | | | |
| ADA/USDT | -2.9% | | | |
| ETH/USDT | -2.8% | | | |
| SOL/USDT | -1.0% | | | |
| BTC/USDT | -0.5% | | | |

Sustained selling pressure over 30 days with declining afternoon selloffs. Long-only strategies were swimming upstream the entire period.

### Manual Strategy Tests (A–G) — All Lost Money

| Test | Entry | Exit Signal | Stoploss | Trades | WR | P&L | PF |
|---|---|---|---|---|---|---|---|
| v7 | MR + TF strict | RSI+BB+EMA | -3% | 15 | 0% | -$1.25 | 0.00 |
| A | EMA cross simple | EMA bear+RSI | -3% | 1289 | 15.6% | -$107 | 0.07 |
| B | EMA cross simple | None | -3% | 1127 | 26.7% | -$95 | 0.16 |
| C | EMA cross+filters | None | -3% | 96 | 43.8% | -$8.96 | 0.22 |
| **D** | **EMA cross+filters** | **None, lower ROI** | **-3%** | **96** | **50%** | **-$8.73** | **0.22** |
| E | EMA cross+filters | None, no ROI | -1.5% | 97 | 43.3% | -$9.45 | 0.16 |
| F | EMA cross+filters | EMA bear cross | -2% | 101 | 29.7% | -$8.50 | 0.12 |
| G | MACD cross+filters | None | -2.5% | 359 | 55.2% | -$26.35 | 0.22 |
| G (15m) | MACD cross+filters | None | -2.5% | 24 | 25% | -$2.73 | 0.07 |

**Key finding across ALL manual tests:** The exit side matters more than the entry side.
- ROI exits: **100% WR** in every test
- profit_protect: **100% WR** in every test
- trailing_stop: **85-93% WR** in every test
- **Every indicator-based exit_signal: 0% WR** — always the #1 source of losses

### Hyperopt Optimization (300 epochs, SharpeHyperOptLossDaily)

| Metric | Value |
|---|---|
| **Trades** | 5 (4W / 1L) |
| **Win rate** | **80%** |
| **Total P&L** | **+$0.201 USDT** |
| **Profit factor** | **4.34** |
| **Sharpe ratio** | **2.53** |
| **Max drawdown** | $0.06 (0.00%) |
| **Avg duration** | 51 min |
| **Market change** | -0.43% (profitable in a down market) |

The optimizer confirmed: be very selective (~5 trades/month), take small profits at +0.4%, don't use indicator-based exit signals.

**Caveat:** 5 trades is a tiny sample with high overfitting risk. Needs 2-4 weeks of live dry-run validation.

**Scaling projections (if backtest holds):**
- $10 stakes: +$0.20/month
- $100 stakes: +$2.01/month
- $1,000 stakes: +$20.10/month (~2% monthly)

---

## Early Backtest Results (Mar 7-12, 5 days)

| # | Config | Trades | W/L | WR | P&L | P&L/trade |
|---|---|---|---|---|---|---|
| 1 | RSI cross + MACD + trend (Day 2) | 10 | 2/8 | 20% | -$1.09 | -$0.109 |
| 2 | RSI zone + MACD + trend | 31 | 12/19 | 39% | -$2.08 | -$0.067 |
| 3 | + candlestick | 3 | 0/3 | 0% | -$0.30 | -$0.100 |
| 4 | + volume | 15 | 5/10 | 33% | -$0.97 | -$0.065 |
| 5 | + ADX | 9 | 3/6 | 33% | -$0.62 | -$0.069 |
| 6 | **+ volume + ADX (v6 entry)** | **2** | **1/1** | **50%** | **-$0.04** | **-$0.021** |
| 7 | + vol + ADX + candle(lookback) | 0 | — | — | — | — |
| 8 | All 8 conditions (v5) | 0 | — | — | — | — |

**Limitation:** 5 days of sparse Kraken data (some pairs heavily forward-filled). Superseded by 30-day results above.

---

## Daily Performance Tracker

| Date | Trades Opened | Trades Closed | Win Rate | Total P&L | Notes |
|---|---|---|---|---|---|
| 2026-03-09 | 26 | 18 | 50% (9W/9L) | -$0.132 closed / -$0.844 total | Full day: morning wins erased by afternoon selloff. No stoploss hits. Need trend filter, fewer pairs, trailing stop. 8 open overnight. |
| 2026-03-10 | 9 (3+6) | 29 cumulative | 62% (18W/11L) | +$0.254 closed / -$0.749 total | Day 2 improvements deployed 7:23 PM Mar 9. Morning: 3 wins (LTC, ADA, SOL). Afternoon: 6 new trades cluster, all red. See Day 2 log. |

---

## Day 2 Observation Log (2026-03-10)

### Improvements Deployed (7:23 PM MST, Mar 9)
- 1h EMA(50) trend filter — block entries when higher TF bearish
- MACD histogram confirmation — momentum must be improving
- Trailing stop — 0.3% trail after 0.5% profit
- Tighter minimal_roi — 2%/1%/0.5% (was 5%/3%/2%/1%)
- Removed APE, MANA, TON from whitelist (stale RSI data)
- max_open_trades 20→10

### Timeline

**7:23 PM Mar 9** — Bot restarted with Day 2 config. 8 open Day 1 legacy trades.

**7:34 PM** — First exit under new rules: AVAX #23 closed **+0.59% via ROI**. Tighter ROI kicking in.

**7:26–7:36 PM** — Rapid exits: MANA #14 (+0.30%), ETH #21 (+0.61% roi), AVAX #23 (+0.59% roi), LINK #24 (+0.66%), SHIB #25 (+0.84% roi). Day 1 positions recovering and closing green.

**8:56 PM** — TON #18 closed -1.24% (removed pair, worst legacy trade).

**10:23 PM** — Evening check. 5 trades still open (XMR, APE, ALGO legacy, LINK, SHIB). Closed P&L back positive at +$0.046.

**12:16 AM Mar 10** — XMR #10 closed -0.38% after 20+ hours. Stubborn but small loss.

**2:11 AM** — APE #20 recovered and closed **+0.57% via ROI**. Removed pair still managed correctly.

**2:31 AM** — LTC #30: **First true Day 2 trade opened and closed +0.33%.** Trend filter let it through, won.

**5:22 AM** — Morning check. Book completely flat. All Day 1 legacy closed. 0 open trades.

**6:11 AM** — ADA #31 opened and closed **+0.51%**. Clean win.

**7:51 AM** — SOL #32 closed **+1.05% via ROI**. Best trade of all time. Tighter ROI locked it in perfectly.

**8:29 AM** — Day 2 scorecard: 3 trades, 3 wins, 100% win rate. Book flat.

**11:11 AM** — ALGO #33 opened. Currently in drawdown.

**11:36 AM** — DOGE #34 opened.

**11:41 AM** — XRP #35 opened. Three trades in 30 min — mini cluster.

**12:02 PM** — ATOM #36 opened.

**12:41 PM** — LINK #37 opened.

**3:11 PM** — ADA #38 opened.

**3:46 PM** — 6 trades open, all red (-0.77% to -2.84%). Afternoon dip repeating Day 1 pattern but smaller scale (6 vs 14 trades). Trend filter reduced pile-up but didn't eliminate it.

**6:06 PM** — ATOM #36 closed **-1.02% via exit_signal**. First Day 2 loss. Open ~6 hours.

**6:19 PM** — 5 open trades remain, all red (-0.88% to -3.08%). ALGO and DOGE worst at ~-3%. Three trades past the 4h duration danger zone (ALGO, DOGE, XRP at 7h). Pattern mirrors Day 1 afternoon but capped at 5 open (vs 14). Day 2 closed: 3W/1L, +$0.087.

**9:41 PM** — ADA #38 closed -0.98% (exit_signal, ~6h). XRP #35 closed -1.14% (~10h). LINK #37 closed -0.33% (~9h). All afternoon cluster losses.

**~10 PM** — ETH #39 opened (new trade). Trend filter let it through.

**11:58 PM** — 3 open: ALGO #33 (-3.20%, 13h), DOGE #34 (**-4.67%**, 13h — worst trade ever), ETH #39 (-0.73%, new). Day 2 closed: 3W/4L. All 4 losses were afternoon cluster trades open 6-10h+. All 3 wins were morning trades closed in 2-3h. **Duration is the strongest predictor of outcome — a 4h force-exit would have saved ~$0.25 in losses today.**

Closed P&L flipped negative at -$0.095. Total P&L -$0.959.

**3:36 AM Mar 11** — ALGO #33 finally closed **-2.77% via exit_signal** after ~23 hours open. Second worst trade.

**~overnight** — XMR #40 opened (new trade). ETH #39 still open (-0.83%).

**4:10 AM** — DOGE #34 still open at **-4.69%** after 34+ hours. Worst trade ever, approaching -5%. This single trade = ~44% of total drawdown.

**5:26 AM** — DOGE #34 finally closed **-3.89% via exit_signal** after **~42 hours**. Recovered slightly from -4.69% low. Longest and worst trade in the bot's history.

**6:21 AM** — ETH #39 closed **+0.27% via exit_signal** (~15h). Small win.

**9:04 AM** — Only XMR #40 open (-0.77%). Book nearly flat. Day 2 final: **4W/6L, -$0.801**. Overall: 19W/17L, closed P&L -$0.736. Avg winner duration 5.8h, avg loser duration 16h. The 4h force-exit case is overwhelming — ALGO+DOGE alone lost $0.67, both open 23-42h.

---

## Day 3 Observation Log (2026-03-11)

### Improvements Deployed (9:07 AM MST)
- **4h force-exit:** `custom_exit()` returns 'force_exit_4h' for any trade that is red and open >4 hours. Based on data showing trades >4h avg -0.13% and ALGO/DOGE losing $0.67 over 23-42h.
- **Removed XTZ, BNB** from whitelist — both 0W/3L, -$0.265 combined drag. Pair count now 15.
- Bot restarted at 9:07 AM. XMR #40 still open (-0.37%), only active trade.

### Timeline

**9:07 AM** — Bot restarted with Day 3 config. 15 pairs, 4h force-exit active. XMR #40 open (-0.37%).

**11:49 AM** — XMR #40 closed **-0.34% via `force_exit_4h`**. 🎯 **First force-exit trigger!** The new rule capped the loss at -0.34% after 4h. Compare: ALGO (-2.77%@23h) and DOGE (-3.89%@42h) from Day 2 without force-exit. This single improvement would have saved ~$0.56 on those two trades alone.

**1:10 PM** — Book completely flat. 0 open trades. Waiting for next entry signal. Overall: 19W/18L, closed P&L -$0.770.

**5:14 PM** — Deployed Day 3b indicators: **Bollinger Bands** (close < lower band), **volume filter** (volume > 20-period avg), **ADX trend strength** (ADX < 25 = ranging market only). Entry now requires 7 conditions.

**5:23 PM** — Deployed Day 3c: **Bullish candlestick pattern confirmation**. Added 6 patterns via ta-lib as OR-group: bullish engulfing, hammer, morning star, dragonfly doji, inverted hammer, piercing line. Any one must be present to enter. Entry now requires **8 conditions** — the full stack:
1. RSI(14) crossed below 30
2. MACD histogram improving
3. Close < Bollinger Band lower (20p, 2std)
4. Volume > 20-period rolling avg
5. ADX(14) < 25 (ranging market)
6. Bullish candlestick pattern present
7. 1h EMA(50) slope >= 0
8. Volume > 0

This is now a proper multi-factor, multi-confirmation entry. Very selective — only the highest-conviction setups will trigger. Bot restarted, running clean.

**6:08 PM** — Ran backtest diagnostic (12 config combos, 5 days of data). Found v5 (8 conditions) produced 0 trades — too restrictive. Key finding: `crossed_below` → RSI zone (`< 30`) is critical. BB and candlestick too restrictive on same candle. Volume + ADX is the optimal filter combo (50% WR, -$0.021/trade).

**6:30 PM** — Deployed **v6 strategy** (backtest-optimized). Major changes:
- Entry: RSI zone (< 30, not cross) + MACD + volume + ADX + trend (6 conditions)
- Exit: RSI > 50 + above BB mid (mean-reversion complete), graduated custom_exit (profit_protect at 0.5%, early_loss_cut at 2h/-1%)
- Stoploss: -3% (was -10%)
- Trailing stop: 0.5% trail after 1% profit (was 0.3% after 0.5%)
- BB and candlestick patterns kept as calculated indicators but removed from entry conditions
- Goal: break-even first, then target 3-5% monthly

**6:41 PM** — Deployed **v7 adaptive dual-mode strategy**. Key insight: market has been trending (ADX > 25 ~71% of the time), and our mean-reversion strategy only works when ADX < 25. v7 adds a **trend-following mode** that activates when ADX > 25:
- Mode A (ranging): Same as v6 — RSI zone < 30 + MACD + volume + ADX < 25 + trend
- Mode B (trending): NEW — EMA(9) crosses above EMA(21) + ADX > 25 + +DI > -DI + MACD > 0 + volume + trend
- Adaptive exits: mean-reversion trades exit fast (profit_protect at 0.5%), trend trades ride longer (profit_lock at 1.5%)
- Enter tags track which mode triggered each trade for analysis
- Backtest: 0 trend_follow signals in sparse 5-day data (need live data to validate)

### Day 2 Trade Results

**Closed (Day 2 new trades only, id > 29):**

| # | Pair | P&L | Exit | Duration |
|---|---|---|---|---|
| #30 | LTC | +0.33% | exit_signal | ~3h |
| #31 | ADA | +0.51% | exit_signal | ~2h |
| #32 | SOL | **+1.05%** | **roi** | ~3h |

**Open (as of 3:46 PM MST):**

| # | Pair | Entry | Current | P&L | Open Since |
|---|---|---|---|---|---|
| #33 | ALGO | $0.087 | $0.0852 | -2.84% | 11:11 AM |
| #34 | DOGE | $0.0958 | $0.0945 | -2.13% | 11:36 AM |
| #35 | XRP | $1.393 | $1.385 | -1.40% | 11:41 AM |
| #36 | ATOM | $1.802 | $1.783 | -1.83% | 12:02 PM |
| #37 | LINK | $8.979 | $8.958 | -1.03% | 12:41 PM |
| #38 | ADA | $0.261 | $0.261 | -0.77% | 3:11 PM |

### New Learnings (Day 2)

**7. ROI Exits Are the Best Improvement**
- ROI exits: 5/5 = **100% win rate**, avg +0.73%
- exit_signal: 13/24 = 54% win rate, avg -0.05%
- The tighter ROI table is the single most impactful Day 2 change
- Trades that hit ROI targets are consistently profitable; RSI-based exits are break-even

**8. Trailing Stop Is Inert**
- 0 trailing stop exits across 29 closed trades
- Trades either hit ROI first or exit via RSI > 70 signal
- The 0.5% activation offset may be too close to the 0.5%@60m ROI threshold — they compete
- **Consider:** Remove trailing stop or separate its range from ROI thresholds

**9. Trade Duration Predicts Outcome**
- < 1 hour: avg +0.78% (best)
- 1–4 hours: avg +0.07% (break-even)
- \> 4 hours: avg -0.13% (losers)
- **Implication:** A 4-hour max trade duration could cut losses on stale positions

**10. XTZ and BNB Are Persistent Losers**
- XTZ: 0W/3L, -$0.128 — worst pair by win rate
- BNB: 0W/3L, -$0.136 — worst pair by P&L
- Combined they account for -$0.265 of drag. Removing them would flip total closed P&L higher.

**11. Afternoon Cluster Still Happens (But Smaller)**
- Day 1: 14 trades piled up in afternoon selloff (no filter)
- Day 2: 6 trades piled up in afternoon dip (with trend filter + max 10)
- The 1h EMA trend filter reduces but doesn't eliminate correlated entries
- All crypto pairs still correlate during broad moves — diversification is limited
- **Consider:** Stricter max_open_trades (e.g., 5) or cooldown period between entries

**12. Best Pairs Identified**
- AVAX (2W/0L), SOL (1W/0L), ADA (2W/0L), DOT (2W/0L) — consistent winners
- These are higher-cap, higher-liquidity pairs with reliable RSI behavior
- Worst: XTZ, BNB, TON — either illiquid or poor RSI characteristics on Kraken

