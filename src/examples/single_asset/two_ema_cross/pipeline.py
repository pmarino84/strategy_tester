import numpy as np
import pandas_ta as ta
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

from ....strategy_tester.backtesting.pipeline.factory import create_backtest_pipeline_with_metrics
from ....strategy_tester.broker_params import BrokerParams
from ....strategy_tester.pipeline.context import Context

def load_data(context: Context):
  context.data = GOOG
  return context

def create_strategy(context: Context):
  class TwoEmaCross(Strategy):
    fast_ma_period=10
    slow_ma_period=20

    def init(self):
      super().init()

      self.fast_ma = self.I(lambda: ta.sma(self.data["Close"].s, self.fast_ma_period))
      self.slow_ma = self.I(lambda: ta.sma(self.data["Close"].s, self.slow_ma_period))
    
    def next(self):
      super().next()

      if crossover(self.fast_ma, self.slow_ma):
        self.buy()
      elif crossover(self.slow_ma, self.fast_ma):
        self.sell()

  context.strategy = TwoEmaCross
  return context

def create_pipeline(
  results_parent_folder: str,
  asset_name: str,
  strategy_name: str,
  broker_params: BrokerParams,
  telegram_bot_token: str,
  telegram_chat_id: str):
  return create_backtest_pipeline_with_metrics(
    load_data,
    create_strategy,
    results_parent_folder,
    asset_name=asset_name,
    strategy_name=strategy_name,
    broker_params= broker_params,
    telegram_bot_token=telegram_bot_token,
    telegram_chat_id=telegram_chat_id)
