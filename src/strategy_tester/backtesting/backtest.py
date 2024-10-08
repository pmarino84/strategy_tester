from typing import Type, Tuple
import pandas as pd
from backtesting import Backtest, Strategy

from ..broker_params import BrokerParams

def run_backtest(
    data: pd.DataFrame,
    strategy: Type[Strategy],
    broker_params: BrokerParams) -> Tuple[pd.Series, Backtest]:
  """
  execute the backtest of the strategy.
  Return the Tuple with the statistics result and the backtest instance.\n

  `data` data to perform the backtest\n
  `strategy` the strategy implementation\n
  `broker_params` Params for the broker\n
  """
  bt = Backtest(
    data,
    strategy,
    cash=broker_params.cash,
    commission=broker_params.commission,
    margin=broker_params.margin,
    trade_on_close=broker_params.trade_on_close,
    hedging=broker_params.hedging,
    exclusive_orders=broker_params.exclusive_orders)
  stats = bt.run()
  return stats, bt
