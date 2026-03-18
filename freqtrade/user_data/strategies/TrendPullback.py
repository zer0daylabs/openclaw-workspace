"""
TrendPullback — Multi-signal trend pullback strategy for 5m crypto

Core idea: Only trade WITH the higher-timeframe trend. Enter on pullbacks
in uptrends, exit via ROI/trailing/custom. No exit_signal (proven loser).

Entry signals:
  1. ema_bounce: Price pulls back near EMA21 and bounces in bullish EMA stack
  2. bb_bounce: Price touches lower Bollinger Band in uptrend and recovers

All entries require:
  - 1h bullish trend (EMA20 > EMA50)
  - Volume above average
  - ADX confirms trend exists
  - RSI not extreme

Exits: Tiered ROI + trailing stop + custom (profit protect, force exit)

Designed for: Kraken, 5m, USDT pairs
"""

import talib.abstract as ta
from datetime import datetime
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    CategoricalParameter,
    IStrategy,
    merge_informative_pair,
)


class TrendPullback(IStrategy):

    INTERFACE_VERSION = 3
    PROCESS_ONLY_NEW_CANDLES = True
    startup_candle_count = 60

    # --- ROI: take profits progressively ---
    minimal_roi = {
        "0": 0.015,
        "30": 0.008,
        "60": 0.003,
        "120": 0,
    }

    # --- Risk management ---
    stoploss = -0.012
    trailing_stop = True
    trailing_stop_positive = 0.003
    trailing_stop_positive_offset = 0.006
    trailing_only_offset_is_reached = True

    # --- Hyperopt: entry parameters ---
    buy_adx_min = IntParameter(default=20, low=12, high=30, space='buy')
    buy_rsi_low = IntParameter(default=35, low=20, high=45, space='buy')
    buy_rsi_high = IntParameter(default=65, low=55, high=75, space='buy')
    buy_volume_mult = DecimalParameter(default=0.7, low=0.3, high=1.5, decimals=1, space='buy')
    buy_bb_rsi_max = IntParameter(default=50, low=35, high=60, space='buy')
    buy_ema_pullback_pct = DecimalParameter(default=0.5, low=0.1, high=1.0, decimals=1, space='buy')
    buy_require_1h_trend = CategoricalParameter([True, False], default=False, space='buy')

    # --- Hyperopt: exit parameters ---
    sell_profit_protect = DecimalParameter(default=0.007, low=0.002, high=0.012, decimals=3, space='sell')
    sell_profit_protect_min_minutes = IntParameter(default=20, low=5, high=60, space='sell')
    sell_force_exit_hours = IntParameter(default=4, low=2, high=8, space='sell')
    sell_rsi_exit = IntParameter(default=69, low=65, high=80, space='sell')

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        return [(pair, '1h') for pair in pairs]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # --- EMAs ---
        dataframe['ema8'] = dataframe['close'].ewm(span=8, adjust=False).mean()
        dataframe['ema21'] = dataframe['close'].ewm(span=21, adjust=False).mean()
        dataframe['ema55'] = dataframe['close'].ewm(span=55, adjust=False).mean()

        # --- RSI ---
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # --- ADX ---
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        # --- MACD histogram (confirmation) ---
        macd_df = qtpylib.macd(dataframe['close'])
        dataframe['macdhist'] = macd_df['histogram']

        # --- Bollinger Bands ---
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_mid'] = bollinger['mid']
        dataframe['bb_upper'] = bollinger['upper']
        dataframe['bb_width'] = (dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_mid']

        # --- Volume filter ---
        dataframe['volume_sma20'] = dataframe['volume'].rolling(window=20).mean()

        # --- 1h informative ---
        if self.dp:
            inf = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe='1h')
            inf['ema20_1h'] = inf['close'].ewm(span=20, adjust=False).mean()
            inf['ema50_1h'] = inf['close'].ewm(span=50, adjust=False).mean()
            inf['rsi_1h'] = ta.RSI(inf, timeperiod=14)
            inf['trend_up_1h'] = (inf['ema20_1h'] > inf['ema50_1h']).astype(int)
            dataframe = merge_informative_pair(dataframe, inf, self.timeframe, '1h', ffill=True)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        adx_min = self.buy_adx_min.value
        rsi_low = self.buy_rsi_low.value
        rsi_high = self.buy_rsi_high.value
        vol_mult = self.buy_volume_mult.value
        bb_rsi_max = self.buy_bb_rsi_max.value
        pullback_pct = self.buy_ema_pullback_pct.value / 100.0

        # --- Common filters ---
        common = (
            (dataframe['adx'] > adx_min) &
            (dataframe['volume'] > dataframe['volume_sma20'] * vol_mult) &
            (dataframe['volume'] > 0)
        )
        if self.buy_require_1h_trend.value:
            common = common & (dataframe.get('trend_up_1h_1h', dataframe.get('trend_up_1h', 0)) == 1)

        # --- Signal 1: EMA Bounce ---
        # Bullish EMA stack + price pulled back near EMA21 + bounced above EMA8
        ema_stack = (
            (dataframe['ema8'] > dataframe['ema21']) &
            (dataframe['ema21'] > dataframe['ema55'])
        )
        pullback_zone = (
            (dataframe['low'] <= dataframe['ema21'] * (1 + pullback_pct))
        )
        bounce = (
            (dataframe['close'] > dataframe['ema8'])
        )
        ema_signal = (
            common &
            ema_stack &
            pullback_zone &
            bounce &
            (dataframe['rsi'] > rsi_low) &
            (dataframe['rsi'] < rsi_high) &
            (dataframe['macdhist'] > 0)
        )
        dataframe.loc[ema_signal, ['enter_long', 'enter_tag']] = (1, 'ema_bounce')

        # --- Signal 2: Bollinger Band Bounce ---
        # Price touched lower BB in an uptrend and recovered
        bb_touch = (
            (dataframe['low'].shift(1) <= dataframe['bb_lower'].shift(1))
        )
        bb_recover = (
            (dataframe['close'] > dataframe['bb_lower'])
        )
        in_uptrend = (
            (dataframe['close'] > dataframe['ema55'])
        )
        bb_signal = (
            common &
            bb_touch &
            bb_recover &
            in_uptrend &
            (dataframe['rsi'] > 25) &
            (dataframe['rsi'] < bb_rsi_max)
        )
        dataframe.loc[bb_signal, ['enter_long', 'enter_tag']] = (1, 'bb_bounce')

        return dataframe

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs):
        trade_minutes = (current_time - trade.open_date_utc).total_seconds() / 60

        # Force exit: negative after N hours
        if trade_minutes >= self.sell_force_exit_hours.value * 60 and current_profit < 0:
            return 'force_exit'

        # Profit protect: lock in small gains
        if (current_profit > self.sell_profit_protect.value and
                trade_minutes >= self.sell_profit_protect_min_minutes.value):
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) > 0:
                last = dataframe.iloc[-1]
                if last.get('rsi', 50) > self.sell_rsi_exit.value:
                    return 'profit_protect_rsi'

        return None

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # No exit signal — ROI/trailing/stoploss/custom handle all exits
        return dataframe
