from backtesting.test import GOOG
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import pandas as pd
import pandas_ta as ta

from strategy_tester.metrics.profits_losses_sum import get_profits_losses_sum_by_dayofweek, get_profits_losses_sum_by_hour, get_profits_losses_sum_by_month

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
trades.set_index("EntryTime", inplace = True)
pnl = trades["PnL"]

def test_get_profits_losses_sum_by_hour_empty():
  assert get_profits_losses_sum_by_hour(pd.Series()).empty

def test_get_profits_losses_sum_by_hour_not_empty():
  assert not get_profits_losses_sum_by_hour(pnl).empty

def test_get_profits_losses_sum_by_dow_empty():
  assert get_profits_losses_sum_by_dayofweek(pd.Series()).empty

def test_get_profits_losses_sum_by_dow_not_empty():
  assert not get_profits_losses_sum_by_dayofweek(pnl).empty

def test_get_profits_losses_sum_by_month_empty():
  assert get_profits_losses_sum_by_month(pd.Series()).empty

def test_get_profits_losses_sum_by_month_not_empty():
  assert not get_profits_losses_sum_by_month(pnl).empty