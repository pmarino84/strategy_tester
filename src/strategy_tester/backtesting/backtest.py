from typing import Type, Tuple
import pandas as pd
from backtesting import Backtest, Strategy

def run_backtest(
    data: pd.DataFrame,
    strategy: Type[Strategy],
    cash: float = 10_000,
    commission: float = .0,
    margin: float = 1.,
    trade_on_close=False,
    hedging=False,
    exclusive_orders=False) -> Tuple[pd.Series, Backtest]:
  """
  execute the backtest of the given strategy and broker params, and return the Tuple with the statistics result and the backtest instance.\n

  `data` data to perform the backtest\n
  `strategy` the strategy implementation\n
  `cash` initial balance of the account\n
  `commission` the broker commission\n
  `margin` the margin for leveraged account (margin=1/leverage)\n
  `trade_on_close` if True close the opened position before to open a new trade\n
  `hedging` if True allow trades in both directions simultaneously\n
  `exclusive_orders` if True there is only one opened trade at time\n
  """
  bt = Backtest(
    data,
    strategy,
    cash=cash,
    commission=commission,
    margin=margin,
    trade_on_close=trade_on_close,
    hedging=hedging,
    exclusive_orders=exclusive_orders)
  stats = bt.run()
  return stats, bt
