# Freqtrade Example Strategy - Simple RSI & MACD
# This is a simple example strategy for dry-run testing

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter, CategoricalParameter, merge_informative_pair
from pandas import DataFrame
from datetime import datetime, timedelta, timezone
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class RsiMacD(IStrategy):
    """
    v8 — Hyperopt-ready adaptive strategy
    Entry: MACD cross or EMA cross, tunable filters (ADX, RSI, volume)
    Exit: ROI/trailing/stoploss/custom (all hyperopt-tunable)
    """

    INTERFACE_VERSION = 3
    PROCESS_ONLY_NEW_CANDLES = True
    startup_candle_count = 50

    # Defaults — hyperopt will override these via roi/stoploss/trailing spaces
    minimal_roi = {
        "0": 0.015,
        "30": 0.008,
        "60": 0.004,
        "120": 0.002,
    }
    stoploss = -0.025
    trailing_stop = True
    trailing_stop_positive = 0.003
    trailing_stop_positive_offset = 0.005
    trailing_only_offset_is_reached = True

    # Hyperopt buy parameters
    buy_adx_threshold = IntParameter(default=20, low=15, high=35, space='buy')
    buy_rsi_max = IntParameter(default=70, low=50, high=75, space='buy')
    buy_volume_mult = DecimalParameter(default=1.0, low=0.5, high=2.0, decimals=1, space='buy')
    buy_entry_type = CategoricalParameter(['macd_cross', 'ema_cross', 'both'], default='macd_cross', space='buy')
    buy_require_trend = CategoricalParameter([True, False], default=True, space='buy')

    # Hyperopt sell parameters
    sell_profit_protect = DecimalParameter(default=0.003, low=0.001, high=0.01, decimals=3, space='sell')
    sell_force_exit_hours = IntParameter(default=6, low=2, high=12, space='sell')

    def informative_pairs(self):
        """Define 1h pairs for trend filter"""
        pairs = self.dp.current_whitelist()
        return [(pair, '1h') for pair in pairs]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Populate all indicators upfront for hyperopt speed"""
        # RSI
        dataframe['rsi'] = qtpylib.rsi(dataframe['close'], window=14)
        
        # 5m MACD (returns DataFrame with 'macd', 'signal', 'histogram' columns)
        macd_df = qtpylib.macd(dataframe['close'])
        dataframe['macd'] = macd_df['macd']
        dataframe['macdsignal'] = macd_df['signal']
        dataframe['macdhist'] = macd_df['histogram']

        # Bollinger Bands (20-period, 2 std dev)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']

        # Volume moving average (20-period) for volume filter
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(window=20).mean()

        # ADX — trend strength (switches between modes)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        # EMA crossover for trend-following mode
        dataframe['ema9'] = dataframe['close'].ewm(span=9, adjust=False).mean()
        dataframe['ema21'] = dataframe['close'].ewm(span=21, adjust=False).mean()
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)

        # Bullish candlestick patterns (ta-lib returns 0/100/-100)
        dataframe['cdl_engulfing'] = ta.CDLENGULFING(dataframe)
        dataframe['cdl_hammer'] = ta.CDLHAMMER(dataframe)
        dataframe['cdl_morningstar'] = ta.CDLMORNINGSTAR(dataframe)
        dataframe['cdl_dragonfly'] = ta.CDLDRAGONFLYDOJI(dataframe)
        dataframe['cdl_invertedhammer'] = ta.CDLINVERTEDHAMMER(dataframe)
        dataframe['cdl_piercing'] = ta.CDLPIERCING(dataframe)
        # Combined: any bullish pattern present (value > 0 = bullish)
        dataframe['bullish_candle'] = (
            (dataframe['cdl_engulfing'] > 0) |
            (dataframe['cdl_hammer'] > 0) |
            (dataframe['cdl_morningstar'] > 0) |
            (dataframe['cdl_dragonfly'] > 0) |
            (dataframe['cdl_invertedhammer'] > 0) |
            (dataframe['cdl_piercing'] > 0)
        ).astype(int)

        # 1h EMA(50) trend filter
        if self.dp:
            informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe='1h')
            informative['ema50'] = informative['close'].ewm(span=50, adjust=False).mean()
            informative['ema50_slope'] = informative['ema50'] - informative['ema50'].shift(1)
            dataframe = merge_informative_pair(dataframe, informative, self.timeframe, '1h', ffill=True)

        return dataframe

    # Entry signal
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Hyperopt-tunable entry with MACD cross, EMA cross, or both"""
        entry_type = self.buy_entry_type.value
        adx_thresh = self.buy_adx_threshold.value
        rsi_max = self.buy_rsi_max.value
        vol_mult = self.buy_volume_mult.value

        # Common filters
        common = (
            (dataframe['adx'] > adx_thresh) &
            (dataframe['rsi'] < rsi_max) &
            (dataframe['volume'] > dataframe['volume_mean_20'] * vol_mult) &
            (dataframe['volume'] > 0)
        )
        if self.buy_require_trend.value:
            common = common & (dataframe['ema50_slope_1h'] >= 0)

        if entry_type == 'macd_cross' or entry_type == 'both':
            dataframe.loc[
                common & qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']),
                ['enter_long', 'enter_tag']] = (1, 'macd_cross')

        if entry_type == 'ema_cross' or entry_type == 'both':
            dataframe.loc[
                common & qtpylib.crossed_above(dataframe['ema9'], dataframe['ema21']),
                ['enter_long', 'enter_tag']] = (1, 'ema_cross')

        return dataframe

    def custom_exit(self, pair: str, trade, current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs):
        """Hyperopt-tunable exits"""
        trade_duration = (current_time - trade.open_date_utc).total_seconds() / 3600

        if trade_duration >= self.sell_force_exit_hours.value and current_profit < 0:
            return 'force_exit'

        if current_profit > self.sell_profit_protect.value and trade_duration >= 0.25:
            return 'profit_protect'

        return None

    # Exit signal
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """No exit signal — ROI/trailing/stoploss/custom handle exits"""
        return dataframe
