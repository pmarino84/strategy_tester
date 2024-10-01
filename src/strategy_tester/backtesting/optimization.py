from typing import Callable, Type, Tuple, Union
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
    exclusive_orders=False,

    maximize: Union[str, Callable[[pd.Series], float]] = 'SQN',
    method: str = 'grid',
    max_tries: Union[int, float] = None,
    constraint: Callable[[dict], bool] = None,
    return_heatmap: bool = False,
    return_optimization: bool = False,
    random_state: int = None,

    **kwargs) -> Tuple[pd.Series, Backtest]:
  if not kwargs:
    raise ValueError('Need some strategy parameters to optimize')
  
  bt = Backtest(
    data,
    strategy,
    cash=cash,
    commission=commission,
    margin=margin,
    trade_on_close=trade_on_close,
    hedging=hedging,
    exclusive_orders=exclusive_orders)
  stats, heatmap = bt.optimize(
    kwargs=kwargs,
    maximize=maximize,
    method=method,
    max_tries=max_tries,
    constraint=constraint,
    return_heatmap=return_heatmap,
    return_optimization=return_optimization,
    random_state=random_state)
  return stats, heatmap, bt
