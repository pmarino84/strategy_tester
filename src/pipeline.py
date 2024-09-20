from typing import Any, Dict, Optional, Union
import pandas as pd
from backtesting.backtesting import Strategy, Backtest
from .broker import BrokerParams

class Context:
  data: Optional[pd.DataFrame]
  strategy: Optional[Strategy]
  stats: Optional[pd.Series]
  bt: Optional[Backtest]
  histogram: Optional[pd.DataFrame]
  metrics: Dict[str, Union[pd.DataFrame, pd.Series]]
  custom: Dict[str, Any]
  result_folder: Optional[str]
  broker_params: Optional[BrokerParams]
  def __init__(self) -> None:
    self.data = None
    self.strategy = None
    self.stats = None
    self.histogram = None
    self.metrics = {}
    self.custom = {}
    self.result_folder = None
    self.broker_params = None
  
  def log(self) -> None:
    print("Data frame:")
    print(self.data)
    print("Statistics:")
    print(self.stats)
    print("Histogram:")
    print(self.histogram)
    print("Equity:")
    print(self.stats["_equity_curve"])
    print("Trades:")
    print(self.stats["_trades"])
    print("Metrics:")
    for key in self.metrics.keys():
      print(key + ':')
      print(self.metrics[key])
    print("Strategy params:")
    print(self.get_strategy_params())
    print("Result folder:")
    print(self.result_folder)
    print("broker params:")
    print(self.broker_params)
  
  def get_strategy_params(self) -> dict:
    params = {}
    for key, value in vars(self.strategy).items():
      if not callable(value) and not key.startswith("__") and not key.startswith("_"):
        params[key] = value
    return params

def pipe(*jobs):
  assert len(jobs) > 0, "Should pass job list"

  class Pipeline:
    def __init__(self) -> None:
      pass
    def run(self):
      context = Context()
      
      for job in jobs:
        print(f"Running job {job.__name__}...")
        context = job(context)
    
  return Pipeline()