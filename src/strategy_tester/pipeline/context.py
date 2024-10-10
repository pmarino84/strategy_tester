from typing import Any, Dict, Optional, Union
import pandas as pd
from backtesting.backtesting import Strategy, Backtest

from ..optimization_params import OptimizationParams
from ..telegram.bot import TelegramBot
from ..broker_params import BrokerParams
from ..utils import get_strategy_params

class Context:
  """Context used by the pipeline runner to maintain the data accross all the job"""
  asset_name: Optional[str]
  """(optional) Asset name like EURUSD, BTCUSDT"""
  strategy_name: Optional[str]
  """(optional) your strategy name"""
  data: Optional[pd.DataFrame]
  """Data of the asset under test"""
  strategy: Optional[Strategy]
  """Your Backtesting.py Strategy class"""
  stats: Optional[pd.Series]
  """Result statistics from the backtest/optimization"""
  heatmap: Optional[pd.Series]
  """(optional) Result heatmap from the optimization"""
  bt: Optional[Backtest]
  """Backtest instance"""
  metrics: Dict[str, Union[pd.DataFrame, pd.Series]]
  """(optional) Calculated metrics from statistics and/or heatmap go here"""
  custom: Dict[str, Any]
  """Dictionary for your custom funcionality if needed"""
  result_folder: Optional[str]
  """(optional) Where to save the report files"""
  broker_params: Optional[BrokerParams]
  """Broker params. see `strategy_tester.broker_params.BrokerParams`."""
  optimization_params: Optional[OptimizationParams]
  """Optimization params. see `strategy_tester.optimization_params.OptimizationParams`."""
  strategy_params_to_optimize: Optional[dict]
  """Strategy params to optimize."""
  telegram_chat_id: Optional[Union[str, int]]
  """(optional) Telegram chat id"""
  telegram_bot: Optional[TelegramBot]
  """(optional) Telegram Bot instance"""
  def __init__(self) -> None:
    self.asset_name = None
    self.strategy_name = None
    self.data = None
    self.strategy = None
    self.stats = None
    self.heatmap = None
    self.metrics = {}
    self.custom = {}
    self.result_folder = None
    self.broker_params = None
    self.optimization_params = None
    self.strategy_params_to_optimize = None
    self.telegram_chat_id = None
    self.telegram_bot = None
  
  def get_strategy_params(self) -> dict:
    """Return a dictionary containing only the strategy params defined by you"""
    return get_strategy_params(self.strategy)

  def __repr__(self) -> str:
    result = "Context:"
    result += f"\n+ Asset name      : {self.asset_name}"
    result += f"\n+ Strategy name   : {self.strategy_name}"
    
    result += f"\n+ Strategy params :"
    params = self.get_strategy_params()
    strategy_param_key_max_length = 0
    for key in params:
      curr_length = len(key)
      if curr_length > strategy_param_key_max_length:
        strategy_param_key_max_length = curr_length
    for key in params:
      empty_space_count = strategy_param_key_max_length - len(key)
      result += f"\n  + {key+' '*empty_space_count}: {params[key]}"
    
    result += f"\n+ Result folder      : {self.result_folder}"
    result += f"\n+ Broker params      : {self.broker_params}"
    result += f"\n+ Optimization params: {self.optimization_params}"
    result += f"\n+ Telegram chat ID   : {self.telegram_chat_id}"

    return result