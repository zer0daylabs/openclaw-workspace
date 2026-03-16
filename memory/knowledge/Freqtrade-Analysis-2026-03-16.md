# Freqtrade Strategy Analysis (2026-03-16)

## Performance Summary
- **Total trades:** 41
- **Winning trades:** 20 (48.78% win rate)
- **Losing trades:** 21
- **Net ROI:** -0.11%
- **Net profit:** -$1.15

## Strategy: RsiMacD

### Entry/Exit Analysis
- **Exit reason: signal** (31 trades)
  - Total profit: -1.10% ❌ strategy entry signals need improvement
  
- **Exit reason: ROI** (6 trades)
  - Total profit: +0.37% ✅ exit strategy working well
  
- **Exit reason: early_loss_cut** (1 trade): -0.13%
- **Exit reason: force_exit** (3 trades): -0.28%

### Key Insights
1. **Entry signals underperform**: -1.10% from signal exits
2. **ROI exit threshold works**: +0.37% from ROI exits
3. **Stop-loss working**: Early cuts limiting major losses
4. **Force exits rare**: Only 3 instances

### Recommendations
- Tweak entry thresholds: RSI period, MACD signal line crossover sensitivity
- Test different timeframes: Currently 5-min, try 15-min or 1-hour
- Optimize ROI exit: Consider adjusting current ≈0.28% target
- Add entry tags: Better tracking of entry conditions

---
Generated: 2026-03-16T16:22:00Z
