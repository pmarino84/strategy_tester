import os
import shutil

import pandas as pd

from ....backtesting.saving import save_backtest_results, save_ohlcv_data, save_trades
from ....metrics.save import save_metrics
from ....pipeline.context import Context
from ....utils.files import create_folder_if_not_exist
from ....utils.strategy_params import get_strategy_params


def clone_streamlit_template(context: Context):
  create_folder_if_not_exist(f"{context.result_folder}/webapp/.streamlit")
  dir = os.path.dirname(os.path.realpath(__file__))
  shutil.copyfile(f"{dir}/template/.streamlit/config.toml", f"{context.result_folder}/webapp/.streamlit/config.toml")
  shutil.copyfile(f"{dir}/template/loaders.py", f"{context.result_folder}/webapp/loaders.py")
  shutil.copyfile(f"{dir}/template/main.py", f"{context.result_folder}/webapp/main.py")

def save_strategy_params_as_text(context: Context):
  """
  Save the strategy params on a text file into the streamlit webapp
  """
  params = get_strategy_params(context.strategy)
  max_length = max(len(key) for key in params.keys())
  text = "Strategy params:"
  for param_name, param_value in params.items():
    key = param_name.ljust(max_length, ' ')
    value = param_value.isoformat() if isinstance(param_value, pd.Timedelta) else param_value
    text += f"\n{key} = {value}"
  
  with open(f"{context.result_folder}/webapp/data/strategy_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

def save_broker_params(context: Context):
  """
  Save the broker params on a text file into the streamlit webapp
  """
  parent_folder = context.result_folder
  params = context.broker_params
  text = "Broker params:"
  text += f"\ncash             = {params.cash}"
  text += f"\ncommission       = {params.commission}"
  text += f"\nmargin           = {params.margin}"
  text += f"\ntrades_on_close  = {params.trade_on_close}"
  text += f"\nhedging          = {params.hedging}"
  text += f"\nexclusive_orders = {params.exclusive_orders}"
  with open(f"{parent_folder}/webapp/data/broker_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

def save_metrics_result(context: Context):
  """
  Save the calculated metrics on csv files into the streamlit webapp
  """
  profits_losses_sum_by_hour = context.metrics["profits_losses_sum_by_hour"]
  profits_losses_sum_by_dow = context.metrics["profits_losses_sum_by_dow"]
  profits_losses_sum_by_month = context.metrics["profits_losses_sum_by_month"]

  profits_losses_by_hour = context.metrics["profits_losses_by_hour"]
  profits_losses_by_dow = context.metrics["profits_losses_by_dow"]
  profits_losses_by_month = context.metrics["profits_losses_by_month"]

  entries_by_hour = context.metrics["entries_by_hour"]
  entries_by_dow = context.metrics["entries_by_dow"]
  entries_by_month = context.metrics["entries_by_month"]

  profits_losses_mean_by_hour = context.metrics["profits_losses_mean_by_hour"]
  profits_losses_mean_by_dow = context.metrics["profits_losses_mean_by_dow"]
  profits_losses_mean_by_month = context.metrics["profits_losses_mean_by_month"]

  profits_by_time_opened = context.metrics["profits_by_time_opened"]
  losses_by_time_opened = context.metrics["losses_by_time_opened"]

  save_metrics(entries_by_hour, entries_by_dow, entries_by_month,
              profits_losses_by_hour, profits_losses_by_dow, profits_losses_by_month,
              profits_losses_mean_by_hour, profits_losses_mean_by_dow, profits_losses_mean_by_month,
              profits_losses_sum_by_hour, profits_losses_sum_by_dow, profits_losses_sum_by_month,
              profits_by_time_opened, losses_by_time_opened,
              f"{context.result_folder}/webapp/data")
  return context

def save_source_data(context: Context):
  create_folder_if_not_exist(f"{context.result_folder}/webapp/data")
  save_strategy_params_as_text(context)
  save_broker_params(context)
  save_backtest_results(context, "webapp/data")
  save_metrics_result(context)
  save_trades(context, "webapp/data")
  save_ohlcv_data(context.data, f"{context.result_folder}/webapp/data")
  return context

def create_streamlit_webapp(context: Context):
  clone_streamlit_template(context)
  save_source_data(context)
  return context