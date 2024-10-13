import asyncio
import os
from datetime import datetime
from typing import Optional

import pandas as pd

from ...backtesting.backtest import run_backtest
from ...backtesting.optimization import run_optimization
from ...backtesting.saving import (save_backtest_results,
                                   save_optimization_results)
from ..broker_params import BrokerParams
from ...metrics.entries_counts import (get_entries_by_dayofweek,
                                       get_entries_by_hour,
                                       get_entries_by_month)
from ...metrics.profits_losses_bars import (get_profits_losses_by_dayofweek,
                                            get_profits_losses_by_hour,
                                            get_profits_losses_by_month)
from ...metrics.profits_losses_by_bar_opened import (
    get_losses_by_time_opened, get_profits_by_time_opened)
from ...metrics.profits_losses_mean import (
    get_profits_losses_mean_by_dayofweek, get_profits_losses_mean_by_hour,
    get_profits_losses_mean_by_month)
from ...metrics.profits_losses_sum import (get_profits_losses_sum_by_dayofweek,
                                           get_profits_losses_sum_by_hour,
                                           get_profits_losses_sum_by_month)
from ...metrics.save import save_metrics
from ..optimization_params import OptimizationParams
from ...pipeline.context import Context
from ...telegram.bot import TelegramBot
from ...utils.strategy_params import get_strategy_params
from ..report.html import report_to_html
from ..report.pdf import report_to_pdf


def get_add_asset_name(asset_name: str):
  """
  Return the function to add the given asset name to the pipeline context

  `asset_name` name of the asset used in the strategy
  """
  def add_asset_name(context: Context):
    context.asset_name = asset_name
    return context
  return add_asset_name

def get_add_strategy_name(strategy_name: str):
  """
  Return the function to add the given strategy name to the pipeline context

  `strategy_name` name of the strategy under backtest/optimization
  """
  def add_strategy_name(context: Context):
    context.strategy_name = strategy_name
    return context
  return add_strategy_name

def get_add_broker_params(broker_params: BrokerParams):
  """
  Return the function to add the given broker params to the pipeline context

  `broker_params` params of the broker
  """
  def add_broker_params(context: Context):
    context.broker_params = broker_params
    return context
  return add_broker_params

def get_add_optimization_params(optimization_params: OptimizationParams):
  """
  Return the function to add the given optimization params to the pipeline context

  `optimization_params` params of the optimization
  """
  def add_optimization_params(context: Context):
    context.optimization_params = optimization_params
    return context
  return add_optimization_params

def get_add_strategy_params_to_optimize(strategy_params_to_optimize: dict):
  """
  Return the function to add the given optimization attributes to the pipeline context

  `strategy_params_to_optimize` strategy attributes to optimize
  """
  def add_strategy_params_to_optimize(context: Context):
    context.strategy_params_to_optimize = strategy_params_to_optimize
    return context
  return add_strategy_params_to_optimize

def get_add_telegram_bot(bot_token: Optional[str], chat_id: Optional[str]):
  """
  Return the function to add the telegram bot attributes to the pipeline context.
  If you don't pass anything the function only return the context

  `bot_token` telegram bot token
  `chat_id` telegram chat id
  """
  def add_telegram_bot(context: Context):
    if bot_token and chat_id:
      context.telegram_chat_id = chat_id
      context.telegram_bot = TelegramBot(bot_token)
    return context
  return add_telegram_bot

def strategy_backtest(context: Context):
  """
  Run the backtest and add the statistics result and the backtester to the pipeline context
  """
  stats, bt = run_backtest(
    context.data,
    context.strategy,
    context.broker_params)
  context.stats = stats
  context.bt = bt
  return context

def strategy_optimization(context: Context):
  """
  Run the optimization and add it's results and the backtester to the pipeline context
  """
  stats, heatmap, bt = run_optimization(
    context.data,
    context.strategy,
    context.broker_params,
    context.optimization_params,
    context.strategy_params_to_optimize)
  context.stats = stats
  context.heatmap = heatmap
  context.bt = bt
  return context

def copy_trades_table(context: Context):
  """
  Copy the trades table from backtest statistics result to the pipeline context.
  Before, convert "EntryTime" and "ExitTime" columns to `pd.Datetime` type and add the column "BarCount" to simplify some metrics calculations.
  """
  trades = context.stats["_trades"].copy()
  trades["EntryTime"] = pd.to_datetime(trades["EntryTime"])
  trades["ExitTime"] = pd.to_datetime(trades["ExitTime"])
  trades["BarsCount"] = trades["ExitBar"] - trades["EntryBar"]
  trades.set_index("EntryTime", inplace=True)
  context.custom["trades_copy"] = trades
  return context

def calc_metrics_step_1_of_5(context: Context):
  """
  Calculate the profits/losses sum by hour/day of week/month and add it to the pipeline context
  """
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_sum_by_hour"] = get_profits_losses_sum_by_hour(trades_pnl)
  context.metrics["profits_losses_sum_by_dow"] = get_profits_losses_sum_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_sum_by_month"] = get_profits_losses_sum_by_month(trades_pnl)
  return context

def calc_metrics_step_2_of_5(context: Context):
  """
  Calculate the profits/losses by hour/day of week/month and add it to the pipeline context
  """
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_by_hour"] = get_profits_losses_by_hour(trades_pnl)
  context.metrics["profits_losses_by_dow"] = get_profits_losses_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_by_month"] = get_profits_losses_by_month(trades_pnl)
  return context

def calc_metrics_step_3_of_5(context: Context):
  """
  Calculate the entries count by hour/day of week/month and add it to the pipeline context
  """
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["entries_by_hour"] = get_entries_by_hour(trades_pnl)
  context.metrics["entries_by_dow"] = get_entries_by_dayofweek(trades_pnl)
  context.metrics["entries_by_month"] = get_entries_by_month(trades_pnl)
  return context

def calc_metrics_step_4_of_5(context: Context):
  """
  Calculate the profits/losses mean by hour/day of week/month and add it to the pipeline context
  """
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_mean_by_hour"] = get_profits_losses_mean_by_hour(trades_pnl)
  context.metrics["profits_losses_mean_by_dow"] = get_profits_losses_mean_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_mean_by_month"] = get_profits_losses_mean_by_month(trades_pnl)
  return context

def calc_metrics_step_5_of_5(context: Context):
  """
  Calculate the profits/losses by bar count opened and add it to the pipeline context
  """
  trades = context.custom["trades_copy"]
  context.metrics["profits_by_time_opened"] = get_profits_by_time_opened(trades)
  context.metrics["losses_by_time_opened"] = get_losses_by_time_opened(trades)
  return context

def _format_current_datetime():
    current_datetime = datetime.now()
    year = str(current_datetime.year)
    month = str(current_datetime.month).rjust(2, "0")
    day = str(current_datetime.day).rjust(2, "0")
    hour = str(current_datetime.hour).rjust(2, "0")
    minute = str(current_datetime.minute).rjust(2, "0")
    return f"{year}{month}{day}{hour}{minute}"

def get_create_results_folder_fn(parent_folder: str):
  """
  Return the function that create the folder where to store the result files and add it's path to the pipeline context
  """
  def create_results_folder(context: Context):
    results_folder_path = f"{parent_folder}/{_format_current_datetime()}"
    context.result_folder = results_folder_path
    if not os.path.exists(results_folder_path):
      os.makedirs(results_folder_path)
    return context
  return create_results_folder

def save_backtest_result(context: Context):
  """
  Save the backtest results on files
  """
  save_backtest_results(context.stats, context.result_folder)
  return context

def save_metrics_result(context: Context):
  """
  Save the calculated metrics on csv files
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
              context.result_folder)
  return context

def save_report_to_pdf(context: Context):
  """
  Save calculated metrics as pdf report
  """
  report_to_pdf(context)
  return context

def save_report_to_html(context: Context):
  """
  Save the report as html
  """
  report_to_html(context)
  return context

def _build_notification_message(context: Context):
  asset_name = context.asset_name or "N/A"
  strategy_name = context.strategy_name or context.strategy.__name__
  stats = context.stats

  statistics: list[str] = []
  # max_len = max([len(index) for index in stats.index])
  for index, value in stats.items():
    if index in ["_trades", "_equity_curve", "_strategy"]:
      continue
    # statistics.append(f"{index.ljust(max_len, ' ')}: {value}")
    statistics.append(f"{index}: {value}")
  
  stats_str = "\n".join(statistics)

  msg = f"{strategy_name} strategy test on {asset_name} finished\n\nStatistics:\n{stats_str}"
  
  if isinstance(context.optimization_params, OptimizationParams):
    strategy_better_params = []
    for param_name, param_value in get_strategy_params(stats["_strategy"]).items():
      if param_name in context.strategy_params_to_optimize:
        strategy_better_params.append(f"{param_name}: {param_value}")
    strategy_better_params_str = "\n".join(strategy_better_params)
    msg += f"\n\nStrategy better params:\n{strategy_better_params_str}"

    msg += "\n\nOptimization params used:"
    for param_name, param_value in vars(context.optimization_params).items():
      if param_name in ["constraint"]:
        continue
      msg += f"\n{param_name}: {param_value}"
  
  msg += "\n\nBroker params used:"
  for param_name, param_value in vars(context.broker_params).items():
    msg += f"\n{param_name}: {param_value}"

  return msg

def send_report_to_telegram_chat(context: Context):
  """
  Send the notification to Telegram chat (if telegram bot info available) to inform the end of the pipeline
  """
  if context.telegram_bot:
    # https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues
    async def notify():
      await context.telegram_bot.send_message(context.telegram_chat_id, _build_notification_message(context))
      await context.telegram_bot.send_document(context.telegram_chat_id, f"{context.result_folder}/report.pdf")
      await context.telegram_bot.send_document(context.telegram_chat_id, f"{context.result_folder}/report.html")
    asyncio.run(notify())

def save_strategy_params_as_text(context: Context):
  """
  Save the strategy params on a text file
  """
  params = get_strategy_params(context.strategy)
  max_length = max(len(key) for key in params.keys())
  text = "Strategy params:"
  for param_name, param_value in params.items():
    key = param_name.ljust(max_length, ' ')
    value = param_value.isoformat() if isinstance(param_value, pd.Timedelta) else param_value
    text += f"\n{key} = {value}"
  
  with open(f"{context.result_folder}/strategy_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

def save_strategy_better_params_as_text(context: Context):
  """
  Save the strategy params on a text file
  """
  params = get_strategy_params(context.strategy)
  max_length = max(len(key) for key in params.keys())
  text = "Strategy params:"
  for param_name, param_value in params.items():
    if param_name in context.strategy_params_to_optimize:
      key = param_name.ljust(max_length, ' ')
      value = param_value.isoformat() if isinstance(param_value, pd.Timedelta) else param_value
      text += f"\n{key} = {value}"
  
  with open(f"{context.result_folder}/strategy_better_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

def save_broker_params(context: Context):
  """
  Save the broker params on a text file
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
  with open(f"{parent_folder}/broker_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

def check_trades_available(context: Context):
  """
  Check if there is trades, if not raise an Error to interrupt the pipeline execution.
  """
  if context.stats["_trades"].empty:
    raise IndexError("No trades found")
  return context

def save_optimization_result(context: Context):
  """
  Save the backtest results on files
  """
  save_optimization_results(context.stats, context.heatmap, context.result_folder)
  return context

def save_optimization_params_as_text(context: Context):
  """
  Save the optimizer params on a text file
  """
  params = vars(context.optimization_params)
  max_length = max(len(key) for key in params.keys())
  text = "Optimization params:"
  for param_name, param_value in params.items():
    if param_name in ["constraint"]:
      continue
    key = param_name.ljust(max_length, ' ')
    value = param_value.isoformat() if isinstance(param_value, pd.Timedelta) else param_value
    text += f"\n{key} = {value}"
  
  with open(f"{context.result_folder}/optimization_params.txt", encoding="utf-8", mode="w+") as file:
    file.write(text)
  return context

