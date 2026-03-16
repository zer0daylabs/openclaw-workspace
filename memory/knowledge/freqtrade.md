# Freqtrade — CB Knowledge Summary

Last updated: 2026-03-15
Proficiency: working
Source: Direct experience building RsiMacD strategy, Freqtrade docs

## What It Is
Open-source cryptocurrency trading bot framework. Supports backtesting, hyperopt optimization, and live/dry-run trading across multiple exchanges.

## Architecture
- Python-based, runs in Docker container
- Strategy files define entry/exit logic using pandas DataFrames
- Uses ccxt library for exchange abstraction
- SQLite for trade database, REST API for control
- Supports multiple timeframes and informative pairs

## Our Use Case
- Running in dry-run mode on Kraken exchange
- Strategy: RsiMacD (RSI + MACD + Bollinger Bands + ADX)
- 20 USDT pairs, 5-minute candles
- $10K simulated wallet, $10 stake per trade
- Docker container: `freqtrade`
- API: http://localhost:8080 (freqtrade:freqtrade)

## Key Commands / API
```bash
# Check bot status
curl -s http://localhost:8080/api/v1/status -u freqtrade:freqtrade | jq

# Start/stop bot
curl -X POST http://localhost:8080/api/v1/start -u freqtrade:freqtrade
curl -X POST http://localhost:8080/api/v1/stop -u freqtrade:freqtrade

# Get profit summary
curl -s http://localhost:8080/api/v1/profit -u freqtrade:freqtrade | jq

# Test strategy (syntax + logic check)
docker exec freqtrade freqtrade test-strategy --strategy RsiMacD

# Backtest
docker exec freqtrade freqtrade backtesting --strategy RsiMacD --timerange 20260301-20260315

# Hyperopt
docker exec freqtrade freqtrade hyperopt --strategy RsiMacD --hyperopt-loss SharpeHyperOptLoss --epochs 100 --spaces buy sell

# Download data
docker exec freqtrade freqtrade download-data --timerange 20260301- -t 5m
```

## Configuration
- Config: `~/.openclaw/workspace/freqtrade/user_data/config.json`
- Strategy: `~/.openclaw/workspace/freqtrade/user_data/strategies/RsiMacD.py`
- Data: mounted at `/freqtrade/user_data` in container

## Integration Points
- CB monitors via API and reports in heartbeat
- STRATEGY-METRICS.md tracks performance
- Standing objective: analyze performance, propose parameter tweaks

## Gotchas
- Bot starts in STOPPED state after container restart — must POST /api/v1/start
- V2→V3 API migration: populate_buy_trend→populate_entry_trend, buy→enter_long
- qtpylib.macd() returns DataFrame, not tuple — unpack carefully
- startup_candle_count must be >= longest indicator period
- RSI anomalies in low-liquidity pairs (TON, SHIB, MANA)
- Afternoon trade clusters indicate market correlation, not independent signals

## Resources
- Docs: https://www.freqtrade.io/en/stable/
- Strategy docs: https://www.freqtrade.io/en/stable/strategy-customization/
- Hyperopt: https://www.freqtrade.io/en/stable/hyperopt/
