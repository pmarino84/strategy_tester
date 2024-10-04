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
    optimization_attributes: dict) -> Tuple[pd.Series, Backtest]:
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
    **optimization_attributes,
    maximize=optimization_params.maximize,
    # method=optimization_params.method, # TODO: da usare quando si potranno gestire i 3 risultati da bt.optimize(...
    method="grid",
    max_tries=optimization_params.max_tries,
    constraint=optimization_params.constraint,
    return_heatmap=True, #return_heatmap=optimization_params.return_heatmap,
    return_optimization=False, #return_optimization=optimization_params.return_optimization,
    random_state=optimization_params.random_state)
  return stats, heatmap, bt
