from typing import Tuple, Type

import pandas as pd
from backtesting import Backtest, Strategy

from .broker_params import BrokerParams
from .optimization_params import OptimizationParams


def run_optimization(
    data: pd.DataFrame,
    strategy: Type[Strategy],
    broker_params: BrokerParams,
    optimization_params: OptimizationParams,
    strategy_params_to_optimize: dict) -> Tuple[pd.Series, pd.DataFrame, Backtest]:
  """
  execute the optimization of the strategy.
  Return the Tuple with the statistics, result heatmap and the backtest instance.\n

  `data` data to perform the optimization\n
  `strategy` the strategy implementation\n
  `broker_params` Params for the broker\n
  `optimization_params` Params for the optimization\n
  `strategy_params_to_optimize` Strategy attributes to optimize\n
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
  stats, heatmap = bt.optimize(
    **strategy_params_to_optimize,
    maximize=optimization_params.maximize,
    # method=optimization_params.method, # TODO: da usare quando si potranno gestire i 3 risultati da bt.optimize(...
    method="grid",
    max_tries=optimization_params.max_tries,
    constraint=optimization_params.constraint,
    return_heatmap=True, #return_heatmap=optimization_params.return_heatmap,
    return_optimization=False, #return_optimization=optimization_params.return_optimization,
    random_state=optimization_params.random_state)
  return stats, heatmap, bt
