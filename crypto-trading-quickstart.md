# Crypto Trading Bot - Quick Start Guide
**Zer0Day Labs Inc.**

---

## 🚀 Getting Started with Freqtrade (Recommended)

### Step 1: Install Prerequisites

```bash
# Ensure you have Python 3.11+
python3 --version

# Install Docker (recommended approach)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Step 2: Deploy Freqtrade via Docker

```bash
# Create user directory structure
mkdir -p freqtrade/user_data/strategies
mkdir -p freqtrade/user_data/data
mkdir -p freqtrade/user_data/logs

# Run Freqtrade in dry-run mode
cd freqtrade

docker run -d \
  --name freqtrade \
  -p 8080:8080 \
  -v $(pwd)/user_data:/freqtrade/user_data \
  freqtradeorg/freqtrade:stable

# Access WebUI at: http://localhost:8080
```

### Step 3: Configure API Keys

1. Go to exchange (e.g., Binance) → API Management
2. Create new API key with **TRADER** permissions only
3. **IMPORTANT:** Enable IP whitelisting (add your server IP)
4. Copy API Key and Secret
5. Store securely using OpenClaw password vault:

```bash
# Using local password vault skill
echo "API_KEY=your_binance_api_key" >> ~/.openclaw/workspace/.env
```

### Step 4: Create Config File

Create `user_data/config.json`:

```json
{
  "stake_currency": "USDT",
  "stake_amount": 10.0,
  "max_open_trades": 3,
  "fiat_display_currency": "USD",
  "timeframe": "5m",
  "dry_run": true,
  "dry_run_wallet": 1000,
  "exchange": {
    "name": "binance",
    "key": "YOUR_API_KEY",
    "secret": "YOUR_API_SECRET",
    "ccxt_config": {},
    "ccxt_async_config": {
      "aiohttp_trust_env": true
    }
  },
  "pairlists": [
    {"method": "StaticPairlist"},
    {"method": "VolumePairlist", "number_assets": 10}
  ],
  "edge": {
    "disabled": true
  }
}
```

### Step 5: Start Trading

```bash
# View bot stats
docker exec freqtrade freqtrade trade --config config.json

# View WebUI
docker exec -it freqtrade freqtrade webserver

# List available strategies
docker exec freqtrade freqtrade list-strategies

# Backtest a strategy
docker exec freqtrade freqtrade backtesting --strategy DefaultStrategy --timerange 20240101-20240201
```

### Step 6: Telegram Integration (Optional)

```json
{
  "telegram": {
    "enabled": true,
    "token": "YOUR_TELEGRAM_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```

Create bot via @BotFather on Telegram, then get your chat ID from @userinfobot

---

## 📊 Paper Trading Strategy

### Conservative Strategy Parameters:
- **Max open trades:** 2-3
- **Stake per trade:** 5-10% of wallet
- **Stop loss:** 3-5%
- **Minimal ROI:** 1-2%
- **Timeframes:** 15m-1h (start larger, scale down)
- **Pairs:** Top 10-20 by volume (BTC, ETH, SOL, etc.)

### Example Default Strategy:

```python
from freqtrade.strategy import IStrategy, merge_infi
from pandas import DataFrame
import talib

class MyFirstStrategy(IStrategy):
    timeframe = '15m'
    stoploss = -0.05  # 5% stop loss
    minimal_roi = {"0": 0.02}  # 2% profit target
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add RSI
        dataframe['rsi'] = talib.RSI(dataframe['close'], timeperiod=14)
        
        # Add MACD
        macd, signal, hist = talib.MACD(dataframe['close'])
        dataframe['macd'] = macd
        dataframe['macd_signal'] = signal
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 45) &  # RSI oversold
                (dataframe['macd'] > dataframe['macd_signal']) &  # MACD cross
                (dataframe['volume'] > 0)
            ),
            'enter_long'
        ] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 70) &  # RSI overbought
                (dataframe['macd'] < dataframe['macd_signal']) &  # MACD cross
                (dataframe['volume'] > 0)
            ),
            'exit_long'
        ] = 1
        
        return dataframe
```

---

## 🔒 Security Checklist

- [ ] API keys stored securely (not in config files)
- [ ] IP whitelisting enabled on exchange
- [ ] Stop-loss configured for all strategies
- [ ] Max daily loss limit set
- [ ] Telegram/Slack alerts configured
- [ ] Bot process monitored (systemd/supervisor)
- [ ] Error logging enabled
- [ ] Git ignore for sensitive files (.env, keys)
- [ ] Regular backups of config and strategies

---

## 📈 Monitoring Commands

```bash
# View current trades
docker exec freqtrade freqtrade trade --config config.json

# Show performance
docker exec freqtrade freqtrade trade --config config.json --show-trades

# Daily profit report
docker exec freqtrade freqtrade trade --config config.json --daily 7

# Check balance
docker exec freqtrade freqtrade trade --config config.json --show-balance

# Force exit all trades (emergency)
docker exec freqtrade freqtrade trade --config config.json --forceexit all
```

---

## 🎯 Next Actions

1. ✅ Deploy Freqtrade in dry-run mode
2. ✅ Connect to Binance testnet/mainnet
3. ✅ Configure monitoring/alerts
4. ✅ Test for 2-4 weeks minimum
5. ✅ Review performance and adjust
6. ✅ Start with small live capital if profitable

---

**Need help?** Check the full research report at `crypto-trading-research.md` for detailed analysis and alternatives.
