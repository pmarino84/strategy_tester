import numpy as np
import pandas as pd
import pandas_ta as ta
from backtesting import Strategy
from backtesting.backtesting import Trade

from ....strategy_tester.backtesting.broker_params import BrokerParams
# from ....strategy_tester.backtesting.pipeline.factory import create_backtest_pipeline_with_metrics
from ....strategy_tester.pipeline.context import Context
from .factory import create_backtest_pipeline_with_metrics_and_fractional_units


def load_csv(file_path: str, datatime_column_name="Date", format="%Y-%m-%d"):
  data = pd.read_csv(file_path)
  data[datatime_column_name] = pd.to_datetime(data[datatime_column_name].str.replace(".000", ""), format=format)
  data.set_index(datatime_column_name, inplace=True)
  return data

def create_load_data(data_file_path: str, datatime_column_name="Date", datetime_format="%Y-%m-%d"):
  def load_data(context: Context):
    context.data = load_csv(data_file_path, datatime_column_name, datetime_format)
    return context
  return load_data

def create_strategy(context: Context):
  data = context.data

  # TODO: add sessions as filter
  # TODO: add EMA24,EMA48 as trend filter (and their slope?)
  # TODO: add RSI50 threshold as filter?
  class StochasticRsiReversalStrategy(Strategy):
    atr_period=10
    rsi_period=14
    rsi_lower_threshold=40
    rsi_higher_threshold=70
    sl_atr_multiplier=1.5
    position_size=0.1

    # exit after N bars
    use_exit_after_timedelta=False
    exit_after_timedelta=pd.Timedelta(70 * 15, unit="minutes") # bar_count * interval

    def init(self):
      super().init()
      self.stoch_rsi = self.I(lambda: ta.stochrsi(data["Close"], length=self.rsi_period, rsi_length=self.rsi_period, k=3, d=3)["STOCHRSIk_14_14_3_3"], name="Stoch. RSI")
      self.atr = self.I(lambda: ta.atr(data["High"], data["Low"], data["Close"], length=self.atr_period), name="ATR")
      # self.atr_lower_band = self.I(lambda: daily_data["Low"] - self.atr * self.sl_atr_multiplier, name="ATR Lower band", color="red")
      # self.atr_upper_band = self.I(lambda: daily_data["High"] + self.atr * self.sl_atr_multiplier, name="ATR Upper band", color="red")
      self.atr_lower_band = self.I(lambda: data["Close"] - self.atr * self.sl_atr_multiplier, name="ATR Lower band", color="red")
      self.atr_upper_band = self.I(lambda: data["Close"] + self.atr * self.sl_atr_multiplier, name="ATR Upper band", color="red")
      self.signal_long = self.I(lambda: self.stoch_rsi < self.rsi_lower_threshold, name="Signal Long", plot=False)
      self.signal_short = self.I(lambda: self.stoch_rsi > self.rsi_higher_threshold, name="Signal Short", plot=False)
    
    def trailing_sl(self, trade: Trade):
      if trade.is_long:
        trade.sl = max(trade.sl or -np.inf, self.atr_lower_band[-1])
      else:
        trade.sl = min(trade.sl or np.inf, self.atr_upper_band[-1])

    def next(self):
      super().next()
      # signal_long = self.stoch_rsi[-1] < self.rsi_lower_threshold
      # signal_short = self.stoch_rsi[-1] > self.rsi_higher_threshold
      signal_long = self.signal_long[-1]
      signal_short = self.signal_short[-1]

      for trade in self.trades:
        if self.use_exit_after_timedelta:
          time_delta = self.data.index[-1] - trade.entry_time
          if (time_delta >= self.exit_after_timedelta):
            trade.close()
        
        self.trailing_sl(trade)

      if len(self.trades) == 0:
        if signal_long:
          self.buy(sl=self.atr_lower_band[-1], size=self.position_size)
        elif signal_short:
          self.sell(sl=self.atr_upper_band[-1], size=self.position_size)

  context.strategy = StochasticRsiReversalStrategy
  return context

def create_pipeline_backtest(
  data_file_path: str,
  datatime_column_name: str,
  datetime_format: str,
  results_parent_folder: str,
  asset_name: str,
  strategy_name: str,
  broker_params: BrokerParams,
  telegram_bot_token: str,
  telegram_chat_id: str):
  return create_backtest_pipeline_with_metrics_and_fractional_units(
    create_load_data(data_file_path, datatime_column_name, datetime_format),
    create_strategy,
    results_parent_folder,
    fraction_unit=1e8, # One satoshi (1e-8 BTC)
    # fraction_unit=1e6, # One micro BTC (μBTC OHLC prices)
    asset_name=asset_name,
    strategy_name=strategy_name,
    broker_params= broker_params,
    telegram_bot_token=telegram_bot_token,
    telegram_chat_id=telegram_chat_id)