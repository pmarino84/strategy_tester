import asyncio
import os
from typing import Optional
import pandas as pd

from ...backtesting.backtest import run_backtest
from ...backtesting.saving import save_backtest_results
from ...broker_params import BrokerParams
from ...metrics.entries_counts import get_entries_by_dayofweek, get_entries_by_hour, get_entries_by_month
from ...metrics.profits_losses_bars import get_profits_losses_by_dayofweek, get_profits_losses_by_hour, get_profits_losses_by_month
from ...metrics.profits_losses_by_bar_opened import get_losses_by_time_opened, get_profits_by_time_opened
from ...metrics.profits_losses_mean import get_profits_losses_mean_by_dayofweek, get_profits_losses_mean_by_hour, get_profits_losses_mean_by_month
from ...metrics.profits_losses_sum import get_profits_losses_sum_by_dayofweek, get_profits_losses_sum_by_hour, get_profits_losses_sum_by_month
from ...metrics.report_pdf import metrics_to_pdf
from ...metrics.save import save_metrics
from ...pipeline.context import Context
from ...telegram.bot import TelegramBot
from ..report_html import report_html as save_report_html

def get_add_asset_name(asset_name: str):
  def add_asset_name(context: Context):
    context.asset_name = asset_name
    return context
  return add_asset_name

def get_add_strategy_name(strategy_name: str):
  def add_strategy_name(context: Context):
    context.strategy_name = strategy_name
    return context
  return add_strategy_name

def get_add_broker_params(broker_params: BrokerParams):
  def add_broker_params(context: Context):
    context.broker_params = broker_params
    return context
  return add_broker_params

def get_add_telegram_bot(bot_token: Optional[str], chat_id: Optional[str]):
  def add_telegram_bot(context: Context):
    if bot_token and chat_id:
      context.telegram_chat_id = chat_id
      context.telegram_bot = TelegramBot(bot_token)
    return context
  return add_telegram_bot

def strategy_backtest(context: Context):
  stats, bt = run_backtest(
    context.data,
    context.strategy,
    context.broker_params.cash,
    context.broker_params.commission,
    context.broker_params.margin,
    context.broker_params.trade_on_close,
    context.broker_params.hedging,
    context.broker_params.exclusive_orders)
  context.stats = stats
  context.bt = bt
  return context

def copy_trades_table(context: Context):
  trades = context.stats["_trades"].copy()
  trades["EntryTime"] = pd.to_datetime(trades["EntryTime"])
  trades["ExitTime"] = pd.to_datetime(trades["ExitTime"])
  trades["BarsCount"] = trades["ExitBar"] - trades["EntryBar"]
  trades.set_index("EntryTime", inplace=True)
  context.custom["trades_copy"] = trades
  return context

def calc_metrics_step_1_of_5(context: Context):
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_sum_by_hour"] = get_profits_losses_sum_by_hour(trades_pnl)
  context.metrics["profits_losses_sum_by_dow"] = get_profits_losses_sum_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_sum_by_month"] = get_profits_losses_sum_by_month(trades_pnl)
  return context

def calc_metrics_step_2_of_5(context: Context):
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_by_hour"] = get_profits_losses_by_hour(trades_pnl)
  context.metrics["profits_losses_by_dow"] = get_profits_losses_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_by_month"] = get_profits_losses_by_month(trades_pnl)
  return context

def calc_metrics_step_3_of_5(context: Context):
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["entries_by_hour"] = get_entries_by_hour(trades_pnl)
  context.metrics["entries_by_dow"] = get_entries_by_dayofweek(trades_pnl)
  context.metrics["entries_by_month"] = get_entries_by_month(trades_pnl)
  return context

def calc_metrics_step_4_of_5(context: Context):
  trades_pnl = context.custom["trades_copy"]["PnL"]
  context.metrics["profits_losses_mean_by_hour"] = get_profits_losses_mean_by_hour(trades_pnl)
  context.metrics["profits_losses_mean_by_dow"] = get_profits_losses_mean_by_dayofweek(trades_pnl)
  context.metrics["profits_losses_mean_by_month"] = get_profits_losses_mean_by_month(trades_pnl)
  return context

def calc_metrics_step_5_of_5(context: Context):
  trades = context.custom["trades_copy"]
  context.metrics["profits_by_time_opened"] = get_profits_by_time_opened(trades)
  context.metrics["losses_by_time_opened"] = get_losses_by_time_opened(trades)
  return context

def strategy_params_to_file_suffix(params: dict):
  file_suffix = ""
  for param_name in params:
    value = params[param_name]
    if isinstance(value, pd.Timedelta):
      value = value.isoformat()
    formatted = f"{param_name}={value}"
    if file_suffix == "":
      file_suffix = formatted
    else:
      file_suffix = f"{file_suffix}|{formatted}"
  file_suffix = f"params=[{file_suffix}]"
  return file_suffix

def broker_params_to_folder_name(params: BrokerParams):
  return f"broker_[cash={params.cash}|commission={params.commission}|margin={params.margin}|trade_on_close={params.trade_on_close}|hedging={params.hedging}|exclusive_orders={params.exclusive_orders}]"

def get_create_results_folder_fn(parent_folder: str):
  def create_results_folder(context: Context):
    results_folder_path = f"{parent_folder}/{broker_params_to_folder_name(context.broker_params)}/{strategy_params_to_file_suffix(context.get_strategy_params())}"
    context.result_folder = results_folder_path
    if not os.path.exists(results_folder_path):
      os.makedirs(results_folder_path)
    return context
  return create_results_folder

def save_backtest_result(context: Context):
  save_backtest_results(context.stats, context.result_folder)
  return context

def save_metrics_result(context: Context):
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

def save_metrics_result_to_pdf(context: Context):
  profits_losses_sum_by_hour = context.metrics["profits_losses_sum_by_hour"]
  profits_losses_sum_by_dow = context.metrics["profits_losses_sum_by_dow"]
  profits_losses_sum_by_month = context.metrics["profits_losses_sum_by_month"]

  profits_losses_by_hour = context.metrics["profits_losses_by_hour"]
  profits_losses_by_dow = context.metrics["profits_losses_by_dow"]
  profits_losses_by_month = context.metrics["profits_losses_by_month"]

  entries_by_hour = context.metrics["entries_by_hour"]
  entries_by_dow = context.metrics["entries_by_dow"]
  entries_by_month = context.metrics["entries_by_month"]

  # profits_losses_mean_by_hour = context.metrics["profits_losses_mean_by_hour"]
  # profits_losses_mean_by_dow = context.metrics["profits_losses_mean_by_dow"]
  # profits_losses_mean_by_month = context.metrics["profits_losses_mean_by_month"]

  profits_by_time_opened = context.metrics["profits_by_time_opened"]
  losses_by_time_opened = context.metrics["losses_by_time_opened"]

  metrics_to_pdf(entries_by_hour, entries_by_dow, entries_by_month,
        profits_losses_by_hour, profits_losses_by_dow, profits_losses_by_month,
        profits_losses_sum_by_hour, profits_losses_sum_by_dow, profits_losses_sum_by_month,
        profits_by_time_opened, losses_by_time_opened,
        context.stats["_equity_curve"]["Equity"], context.stats,
        f"{context.result_folder}/metrics.pdf")
  return context

def get_report_html_fn(strategy_name: str = None):
  def report_html(context: Context):
    save_report_html(context, context.result_folder, strategy_name=strategy_name)
    return context
  return report_html

def send_report_to_telegram_chat(context: Context):
  if context.telegram_bot:
    asset_name = context.asset_name or "N/A"
    strategy_name = context.strategy_name or context.strategy.__name__
    # https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues
    async def notify():
      await context.telegram_bot.send_message(context.telegram_chat_id, f"{asset_name} {strategy_name} strategy backtest finished")
    asyncio.run(notify())