# Freqtrade Hyperopt — CB Knowledge Summary

Last updated: 2026-03-18
Proficiency: basic (research complete)
Domain: Trading strategy optimization

---

## What It Is

Freqtrade Hyperopt is a hyperparameter optimization framework that:
- **Optimizes strategy parameters** using Bayesian search algorithms
- Uses **optuna**'s NSGAIIISampler for efficient hyperspace search
- Runs **many backtests** with different parameter combinations
- Minimizes **custom loss function** values to find best parameters
- Finds optimal **buy/sell/stoploss/ROI/trailing** parameters

---

## Installation

```bash
# Install hyperopt dependencies (not included in base install)
pip install -r requirements-hyperopt.txt
# OR use Docker image (includes all dependencies)
```

---

## Command Reference

### Basic Hyperopt Command
```bash
freqtrade hyperopt \
  --strategy RsiMacD \
  --hyperopt-loss SharpeHyperOptLoss \
  --timerange 20230101-20230630 \
  --epochs 100 \
  --spaces buy,stoploss,roi,sell \
  -j -1  # use all CPU cores
```

### Key Parameters

- `--strategy`: Strategy class name
- `--hyperopt-loss`: Loss function class name
- `--timerange`: Data period (YYYYMMDD-YYYYMMDD)
- `--epochs`: Number of iterations (default: 100)
- `--spaces`: Which parameters to optimize
- `-j/--job-workers`: Parallel workers (-1=all CPUs, 1=sequential)
- `--random-state`: For reproducibility
- `--min-trades`: Minimum desired trades
- `--early-stop`: Stop after N epochs without improvement

### Available Spaces
- `default` - buy, stoploss, roi (basic optimization)
- `buy` - entry signal parameters
- `sell` - exit signal parameters
- `enter` - enter signal parameters (modern syntax)
- `exit` - exit signal parameters (modern syntax)
- `stoploss` - stop loss optimization
- `roi` - ROI table optimization
- `trailing` - trailing stop optimization
- `all` - all parameters
- `protection` - protection parameters
- `trades` - max_open_trades

---

## Hyperopt Loss Functions

Built-in loss functions (all minimize to find best parameters):

1. **SharpeHyperOptLoss** - Optimizes Sharpe ratio
2. **SharpeHyperOptLossDaily** - Sharpe ratio normalized per day
3. **SortinoHyperOptLoss** - Sortino ratio (downside volatility only)
4. **SortinoHyperOptLossDaily** - Sortino ratio per day
5. **MaxDrawDownHyperOptLoss** - Minimizes max drawdown
6. **MaxDrawDownRelativeHyperOptLoss** - Relative drawdown
7. **ProfitDrawDownHyperOptLoss** - Balance profit and drawdown
8. **OnlyProfitHyperOptLoss** - Maximize total profit only
9. **ShortTradeDurHyperOptLoss** - Optimizes for short trades

---

## Key Best Practices

### Data Quality
- **Use 6+ months of data** for reliable optimization
- Too short → overfitting to specific market conditions
- Run multiple times with different timeranges

### Reproducibility
- Set `--random-state INT` for consistent results
- Run with different seeds to compare outcomes
- Hyperopt is non-deterministic without fixed seed

### Performance
- **Requires 2+ CPU cores** - crashes on single core
- `-j -1` uses all available cores
- Not recommended for Raspberry Pi - too CPU intensive

### Space Definition
- **populate_indicators** must create ALL indicators used by any space
- Missing indicators will cause hyperopt to fail
- Define parameters with `space='buy'`, `space='sell'`, etc.

### Trade Duration
- Current strategy: `--timerange 20230101-20230630` (6 months)
- Longer timeranges give more robust results
- Multiple runs help validate stability

---

## Custom Hyperopt Loss Function

To create custom loss function:

```python
from datetime import datetime
from typing import Any, Dict
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss

class MyCustomLoss(IHyperOptLoss):
    TARGET_TRADES = 600
    EXPECTED_MAX_PROFIT = 3.0
    MAX_ACCEPTED_TRADE_DURATION = 300

    @staticmethod
    def hyperopt_loss_function(
        *,
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        **kwargs
    ) -> float:
        """Returns float - smaller = better"""
        total_profit = results['profit_ratio'].sum()
        trade_duration = results['trade_duration'].mean()
        
        trade_loss = 1 - 0.25 * exp(-(trade_count - 600) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - total_profit / 3.0)
        duration_loss = 0.4 * min(trade_duration / 300, 1)
        
        return trade_loss + profit_loss + duration_loss
```

**Loss function receives:**
- `results` DataFrame with all trade data
- `trade_count`: Total trades
- `min_date`, `max_date`: Timerange used
- `config`: Configuration object
- `processed`: Dict of DataFrames with pair data
- `backtest_stats`: Backtest statistics
- `starting_balance`: Starting capital

---

## Advanced: Custom Spaces

Override default parameter ranges via nested `HyperOpt` class:

```python
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def stoploss_space():
            return [SKDecimal(-0.05, -0.01, decimals=3, name='stoploss')]

        def roi_space() -> List[Dimension]:
            return [
                Integer(10, 120, name='roi_t1'),
                Integer(10, 60, name='roi_t2'),
                Integer(10, 40, name='roi_t3'),
                SKDecimal(0.01, 0.04, decimals=3, name='roi_p1'),
                SKDecimal(0.01, 0.07, decimals=3, name='roi_p2'),
                SKDecimal(0.01, 0.20, decimals=3, name='roi_p3'),
            ]

        def generate_roi_table(params: Dict) -> dict[int, float]:
            # ... custom ROI table logic
            return roi_table

        def trailing_space() -> List[Dimension]:
            # ... custom trailing stop space
            pass

        def max_open_trades_space() -> List[Dimension]:
            return [Integer(-1, 10, name='max_open_trades')]
```

---

## Advanced: Custom Samplers

Override the base estimator to use different optuna samplers:

```python
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def generate_estimator(dimensions: List['Dimension'], **kwargs):
            return "NSGAIIISampler"  # or TPESampler, GPSampler, CmaEsSampler, QMCSampler
```

**Available samplers:**
- `NSGAIISampler` - Good general purpose
- `TPESampler` - Tree-structured Parzen Estimator
- `GPSampler` - Gaussian process-based
- `CmaEsSampler` - Covariance matrix adaptation
- `NSGAIIISampler` - **Most versatile** (default)
- `QMCSampler` - Quasi-Monte Carlo
- `AutoSampler` - Automatic selection from optunahub

**To use AutoSampler:**
```bash
pip install optunahub cmaes torch scipy
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def generate_estimator(dimensions, **kwargs):
            if "random_state" in kwargs:
                return optunahub.load_module("samplers/auto_sampler").AutoSampler(seed=kwargs["random_state"])
            return optunahub.load_module("samplers/auto_sampler").AutoSampler()
```

---

## Space Types

### Categorical
```python
Categorical(['a', 'b', 'c'], name='cat')
# Pick from discrete categories
```

### Integer
```python
Integer(1, 10, name='x')
# Pick from range 1-10 (whole numbers)
```

### SKDecimal (Freqtrade-specific, faster)
```python
SKDecimal(0.1, 0.5, decimals=3, name='x')
# Decimal range with limited precision
```

### Real
```python
Real(0.1, 0.5, name='x')
# Full precision decimal range
```

---

## Our Use Case for Zer0Day Labs

**Current Strategy:** BBMomentum (Bollinger Band squeeze)

**Optimization Goals:**
1. Improve entry timing (BBMOMENTUM_RSI, RSI values)
2. Optimize stoploss levels (-0.015 current)
3. Tune trailing stop parameters
4. Optimize ROI table structure
5. Reduce drawdown while maintaining profit

**Recommended Approach:**
- Start with `SortinoHyperOptLossDaily` for risk-adjusted returns
- Use 6+ month timerange
- Run with different random states
- Compare results against current manual parameters

---

## Gotchas & Warnings

1. **Single CPU core crashes hyperopt** - need minimum 2 cores
2. **populate_indicators must create ALL indicators** - missing ones cause failures
3. **Cannot effectively run on Raspberry Pi** - too CPU intensive
4. **Timerange too short → overfitting** - use 6+ months
5. **Non-deterministic without fixed seed** - use --random-state for reproducibility
6. **Loss function called every epoch** - keep it optimized
7. **Position stacking (eps)** - only for backtesting, not real trading
8. **Protections slow hyperopt considerably** - enable only if critical

---

## Resources

- **Official Docs**: https://www.freqtrade.io/en/stable/hyperopt/
- **Advanced Hyperopt**: https://www.freqtrade.io/en/stable/advanced-hyperopt/
- **Hyperopt-Loss GitHub Issue**: https://github.com/freqtrade/freqtrade/issues/8810 (custom loss examples)
- **Tutorial**: https://dev.to/itrade_icu_ae8778833e3e8c/chapter-5-how-to-optimize-strategy-parameters-freqtrade-hyperopt-quick-start-i6k
- **Sample Hyperopt Loss**: https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_loss.py

---

## Next Steps for Zer0Day Labs

**Phase 1 - Baseline Hyperopt:**
1. Install hyperopt dependencies
2. Run with current BBMomentum strategy
3. Use SortinoHyperOptLossDaily
4. Timerange: 2025-09-01 to 2026-03-18
5. Compare results to manual parameters

**Phase 2 - Custom Optimization:**
1. Analyze current strategy weaknesses
2. Define custom spaces if needed
3. Create custom loss function targeting our objectives
4. Run extended optimization

**Phase 3 - Deployment:**
1. Backtest winning parameters
2. Dry-run verification
3. Deploy if results robust
