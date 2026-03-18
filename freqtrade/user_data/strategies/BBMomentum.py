"""
BBMomentum — Market-neutral Bollinger Band + momentum strategy for 5m crypto

Works in ANY market condition (trending, ranging, bear, bull) by trading
volatility patterns rather than requiring a specific trend direction.

Entry signals:
  1. bb_bounce: Price touches/pierces lower BB then recovers — mean reversion
  2. bb_squeeze: Bollinger Band width contracts then price breaks upward — breakout
  3. volume_spike: Abnormal volume with bullish candle + favorable RSI — momentum

Exits: Tiered ROI + trailing stop + custom (profit protect, force exit)
No exit_signal (proven loser in previous strategies).

Designed for: Kraken, 5m, USDT pairs, $10 stakes
"""

import numpy as np
import talib.abstract as ta
from datetime import datetime
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    merge_informative_pair,
)


class BBMomentum(IStrategy):

    INTERFACE_VERSION = 3
    PROCESS_ONLY_NEW_CANDLES = True
    startup_candle_count = 60

    # --- ROI: take profits progressively ---
    minimal_roi = {
        "0": 0.015,
        "30": 0.008,
        "60": 0.004,
        "120": 0,
    }

    # --- Risk management ---
    stoploss = -0.015
    trailing_stop = True
    trailing_stop_positive = 0.004
    trailing_stop_positive_offset = 0.008
    trailing_only_offset_is_reached = True

    # --- Hyperopt: entry parameters ---
    buy_bb_rsi_max = IntParameter(default=35, low=25, high=55, space='buy')
    buy_squeeze_threshold = DecimalParameter(default=0.04, low=0.01, high=0.06, decimals=2, space='buy')
    buy_volume_spike_mult = DecimalParameter(default=2.5, low=1.5, high=3.0, decimals=1, space='buy')
    buy_spike_rsi_low = IntParameter(default=40, low=30, high=50, space='buy')
    buy_spike_rsi_high = IntParameter(default=58, low=55, high=70, space='buy')
    buy_adx_min = IntParameter(default=20, low=10, high=25, space='buy')

    # --- Hyperopt: exit parameters ---
    sell_profit_protect = DecimalParameter(default=0.005, low=0.002, high=0.012, decimals=3, space='sell')
    sell_profit_protect_min_minutes = IntParameter(default=10, low=5, high=45, space='sell')
    sell_early_loss_minutes = IntParameter(default=30, low=15, high=60, space='sell')
    sell_early_loss_threshold = DecimalParameter(default=-0.003, low=-0.008, high=-0.001, decimals=3, space='sell')
    sell_force_exit_hours = IntParameter(default=2, low=1, high=6, space='sell')

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        return [(pair, '1h') for pair in pairs]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # --- Bollinger Bands ---
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_mid'] = bollinger['mid']
        dataframe['bb_upper'] = bollinger['upper']
        dataframe['bb_width'] = (dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_mid']
        dataframe['bb_width_min'] = dataframe['bb_width'].rolling(window=20).min()

        # --- RSI ---
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # --- ADX ---
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        # --- Volume ---
        dataframe['volume_sma20'] = dataframe['volume'].rolling(window=20).mean()

        # --- EMA for trend context (soft filter) ---
        dataframe['ema50'] = dataframe['close'].ewm(span=50, adjust=False).mean()

        # --- MACD histogram ---
        macd_df = qtpylib.macd(dataframe['close'])
        dataframe['macdhist'] = macd_df['histogram']

        # --- Candle body (bullish = close > open) ---
        dataframe['bullish_candle'] = (dataframe['close'] > dataframe['open']).astype(int)

        # --- 1h RSI for overbought filter ---
        if self.dp:
            inf = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe='1h')
            inf['rsi_1h'] = ta.RSI(inf, timeperiod=14)
            dataframe = merge_informative_pair(dataframe, inf, self.timeframe, '1h', ffill=True)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        bb_rsi_max = self.buy_bb_rsi_max.value
        squeeze_thresh = self.buy_squeeze_threshold.value
        vol_spike = self.buy_volume_spike_mult.value
        spike_rsi_low = self.buy_spike_rsi_low.value
        spike_rsi_high = self.buy_spike_rsi_high.value
        adx_min = self.buy_adx_min.value

        # --- Common filter ---
        common = (dataframe['volume'] > 0)

        # --- Signal 1: BB Bounce (mean reversion) ---
        # Previous candle touched/pierced lower BB, current candle recovered above it
        bb_bounce = (
            common &
            (dataframe['low'].shift(1) <= dataframe['bb_lower'].shift(1)) &
            (dataframe['close'] > dataframe['bb_lower']) &
            (dataframe['rsi'] < bb_rsi_max) &
            (dataframe['rsi'] > 20) &
            (dataframe['bullish_candle'] == 1) &
            (dataframe['volume'] > dataframe['volume_sma20'] * 0.5)
        )
        dataframe.loc[bb_bounce, ['enter_long', 'enter_tag']] = (1, 'bb_bounce')

        # --- Signal 2: BB Squeeze Breakout ---
        # BB width at 20-period low (consolidation), price breaks above mid BB
        squeeze_active = (
            dataframe['bb_width'] <= dataframe['bb_width_min'] * (1 + squeeze_thresh)
        )
        breakout = (
            common &
            squeeze_active.shift(1) &
            (dataframe['close'] > dataframe['bb_mid']) &
            (dataframe['close'].shift(1) <= dataframe['bb_mid'].shift(1)) &
            (dataframe['volume'] > dataframe['volume_sma20']) &
            (dataframe['adx'] > adx_min) &
            (dataframe['macdhist'] > 0)
        )
        dataframe.loc[breakout, ['enter_long', 'enter_tag']] = (1, 'bb_squeeze')

        # --- Signal 3: Volume Spike ---
        # Abnormal volume with bullish candle and favorable RSI
        vol_signal = (
            common &
            (dataframe['volume'] > dataframe['volume_sma20'] * vol_spike) &
            (dataframe['bullish_candle'] == 1) &
            (dataframe['rsi'] > spike_rsi_low) &
            (dataframe['rsi'] < spike_rsi_high) &
            (dataframe['close'] > dataframe['ema50']) &
            (dataframe['macdhist'] > dataframe['macdhist'].shift(1))
        )
        dataframe.loc[vol_signal, ['enter_long', 'enter_tag']] = (1, 'vol_spike')

        return dataframe

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs):
        trade_minutes = (current_time - trade.open_date_utc).total_seconds() / 60

        # Early loss cut: if still losing after N minutes, exit small
        if (trade_minutes >= self.sell_early_loss_minutes.value and
                current_profit < self.sell_early_loss_threshold.value):
            return 'early_loss_cut'

        # Force exit: negative after N hours
        if trade_minutes >= self.sell_force_exit_hours.value * 60 and current_profit < 0:
            return 'force_exit'

        # Profit protect: lock in gains when RSI getting high
        if (current_profit > self.sell_profit_protect.value and
                trade_minutes >= self.sell_profit_protect_min_minutes.value):
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) > 0:
                last = dataframe.iloc[-1]
                if last.get('rsi', 50) > 70:
                    return 'profit_protect_rsi'

        return None

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # No exit signal — ROI/trailing/stoploss/custom handle all exits
        return dataframe
