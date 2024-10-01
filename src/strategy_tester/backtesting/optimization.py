from typing import Type, Tuple
import pandas as pd
from backtesting import Backtest, Strategy

from ..optimization_params import OptimizationParams
from ..broker_params import BrokerParams

def run_optimization(
    data: pd.DataFrame,
    strategy: Type[Strategy],
    broker_params: BrokerParams,
    optimization_params: OptimizationParams,

    **kwargs) -> Tuple[pd.Series, Backtest]:
  if not kwargs:
    raise ValueError('Need some strategy parameters to optimize')
  
  bt = Backtest(
    data,
    strategy,
    cash=broker_params.cash,
    commission=broker_params.commission,
    margin=broker_params.margin,
    trade_on_close=broker_params.trade_on_close,
    hedging=broker_params.hedging,
    exclusive_orders=broker_params.exclusive_orders)
  stats, heatmap = bt.optimize(
    **kwargs,
    maximize=optimization_params.maximize,
    method=optimization_params.method,
    max_tries=optimization_params.max_tries,
    constraint=optimization_params.constraint,
    return_heatmap=optimization_params.return_heatmap,
    return_optimization=optimization_params.return_optimization,
    random_state=optimization_params.random_state)
  return stats, heatmap, bt
