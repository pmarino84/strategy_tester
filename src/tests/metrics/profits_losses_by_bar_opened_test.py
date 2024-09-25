from backtesting.test import GOOG
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import pandas as pd
import pandas_ta as ta

from strategy_tester.metrics.profits_losses_by_bar_opened import get_losses_by_time_opened, get_profits_by_time_opened

class TwoEmaCross(Strategy):
  fast_ma_period = 10
  slow_ma_period = 20
  def init(self):
    super().init()
    self.fast_ma = self.I(ta.ema, self.data["Close"].s, self.fast_ma_period)
    self.slow_ma = self.I(ta.ema, self.data["Close"].s, self.slow_ma_period)
  
  def next(self):
    super().next()
    if crossover(self.fast_ma, self.slow_ma):
      self.position.close()
      self.buy()
    elif crossover(self.slow_ma, self.fast_ma):
      self.position.close()
      self.sell()

bt = Backtest(GOOG, TwoEmaCross)

stats = bt.run()
trades = stats["_trades"].copy()
trades["BarsCount"] = trades["ExitBar"] - trades["EntryBar"]

def test_get_profits_by_time_opened_empty():
  assert get_profits_by_time_opened(pd.DataFrame()).empty

def test_get_profits_by_time_opened_not_empty():
  assert not get_profits_by_time_opened(trades).empty

def test_get_losses_by_time_opened_empty():
  assert get_losses_by_time_opened(pd.DataFrame()).empty

def test_get_losses_by_time_opened_not_empty():
  assert not get_losses_by_time_opened(trades).empty
