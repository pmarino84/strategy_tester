from typing import Type, Tuple
import pandas as pd
from backtesting import Backtest, Strategy

def run_optimization(
    data: pd.DataFrame,
    strategy: Type[Strategy],
    cash: float = 10_000,
    commission: float = .0,
    margin: float = 1.,
    trade_on_close=False,
    hedging=False,
    exclusive_orders=False) -> Tuple[pd.Series, Backtest]:
  raise NotImplementedError()
  # bt = Backtest(
  #   data,
  #   strategy,
  #   cash=cash,
  #   commission=commission,
  #   margin=margin,
  #   trade_on_close=trade_on_close,
  #   hedging=hedging,
  #   exclusive_orders=exclusive_orders)
  # stats, heatmap = bt.optimize()
  # return stats, heatmap, bt
