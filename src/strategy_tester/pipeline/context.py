from typing import Any, Dict, Optional, Union

import pandas as pd
from backtesting.backtesting import Backtest, Strategy

from ..backtesting.broker_params import BrokerParams
from ..backtesting.optimization_params import OptimizationParams
from ..telegram.bot import TelegramBot
from ..utils.strategy_params import get_strategy_params

class Context:
  """Context used by the pipeline runner to maintain the data accross all the job

  Attributes:

  `asset_name` (str): Asset name (like EURUSD, BTCUSDT, NVDAUSD, ...)

  `strategy_name` (str): Name of the strategy under test
  
  `data` (pd.DataFrame): Data of the asset under test
  
  `strategy` (Strategy): Backtesting.py Strategy class implementation
  
  `stats` (pd.Series): Result statistics from the backtest/optimization
  
  `heatmap` (pd.Series): Result heatmap from the optimization, available only with optimization pipelines
  
  `bt` (Backtest): Backtest instance
  
  `metrics` (Dict[str, Union[pd.DataFrame, pd.Series]]): Calculated metrics from statistics and/or heatmap go here
  
  `custom` (Dict[str, any]): Dictionary for your custom funcionality if needed
  
  `result_folder` (str): Where to save the report files
  
  `broker_params` (strategy_tester.backtesting.broker_params.BrokerParams): Broker params
  
  `optimization_params` (strategy_tester.backtesting.optimization_params.OptimizationParams): [optional] Optimization params
  
  `strategy_params_to_optimize` (dict): [optional] Strategy params to optimize
  
  `telegram_chat_id` (Union[str, int]): [optional] Telegram chat id
  
  `telegram_bot` (TelegramBot): [optional] Telegram Bot instance
  """
  asset_name: Optional[str]
  strategy_name: Optional[str]
  data: Optional[pd.DataFrame]
  strategy: Optional[Strategy]
  stats: Optional[pd.Series]
  heatmap: Optional[pd.Series]
  bt: Optional[Backtest]
  metrics: Dict[str, Union[pd.DataFrame, pd.Series]]
  custom: Dict[str, Any]
  result_folder: Optional[str]
  broker_params: Optional[BrokerParams]
  optimization_params: Optional[OptimizationParams]
  strategy_params_to_optimize: Optional[dict]
  telegram_chat_id: Optional[Union[str, int]]
  telegram_bot: Optional[TelegramBot]
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