from typing import Any, Dict, Optional, Union
import pandas as pd
from backtesting.backtesting import Strategy, Backtest
from ..telegram.bot import TelegramBot
from ..broker_params import BrokerParams

class Context:
  asset_name: Optional[str]
  strategy_name: Optional[str]
  data: Optional[pd.DataFrame]
  strategy: Optional[Strategy]
  stats: Optional[pd.Series]
  bt: Optional[Backtest]
  histogram: Optional[pd.DataFrame]
  metrics: Dict[str, Union[pd.DataFrame, pd.Series]]
  custom: Dict[str, Any]
  result_folder: Optional[str]
  broker_params: Optional[BrokerParams]
  telegram_chat_id: Optional[Union[str, int]]
  telegram_bot: Optional[TelegramBot]
  def __init__(self) -> None:
    self.asset_name = None
    self.strategy_name = None
    self.data = None
    self.strategy = None
    self.stats = None
    self.histogram = None
    self.metrics = {}
    self.custom = {}
    self.result_folder = None
    self.broker_params = None
    self.telegram_chat_id = None
    self.telegram_bot = None
  
  def get_strategy_params(self) -> dict:
    params = {}
    for key, value in vars(self.strategy).items():
      if not callable(value) and not key.startswith("__") and not key.startswith("_"):
        params[key] = value
    return params

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
    
    result += f"\n+ Result folder   : {self.result_folder}"
    result += f"\n+ Broker params   : {self.broker_params}"
    result += f"\n+ Telegram chat ID: {self.telegram_chat_id}"

    return result