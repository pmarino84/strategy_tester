import os
import pandas as pd
from ..pipeline import pipe, Context
from .backtest import run_backtest
from .saving import save_backtest_results
from ..metrics import get_entries_by_hour, get_entries_by_dayofweek, get_entries_by_month
from ..metrics import get_profits_losses_by_hour, get_profits_losses_by_dayofweek, get_profits_losses_by_month
from ..metrics import get_profits_by_time_opened, get_losses_by_time_opened
from ..metrics import get_profits_losses_mean_by_hour, get_profits_losses_mean_by_dayofweek, get_profits_losses_mean_by_month
from ..metrics import get_profits_losses_sum_by_hour, get_profits_losses_sum_by_dayofweek, get_profits_losses_sum_by_month
from ..metrics import save_metrics, metrics_to_pdf
from .report_html import report_html as save_report_html
from ..broker import BrokerParams, BrokerParamsBuilder

def get_add_broker_params(broker_params: BrokerParams):
  def add_broker_params(context: Context):
    context.broker_params = broker_params
    return context
  return add_broker_params

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

def create_report_html_fn(strategy_name: str = None):
  def report_html(context: Context):
    save_report_html(context, context.result_folder, strategy_name=strategy_name)
    return context
  return report_html

# TODO: i parametri per il broker meglio passarli come dictionary,
#       anche a create_strategy_backtest ed run_backtest
#       sarà poi run_backtest ad usarli nella maniera corretta
# TODO: con le metriche profits/losses by time opened provare a mostrare il timedelta
# TODO: sistemare le funzioni che salvano i report in pdf/html nel caso non ci siano profitti/perdite si rompe tutto
def create_standar_backtest_pipeline(load_data,
                                    create_strategy,
                                    results_folder_path,
                                    strategy_name: str = None,
                                    broker_params: BrokerParams = BrokerParamsBuilder().build()):
  return pipe(
    load_data,
    create_strategy,
    get_add_broker_params(broker_params),
    strategy_backtest,
    copy_trades_table,
    calc_metrics_step_1_of_5,
    calc_metrics_step_2_of_5,
    calc_metrics_step_3_of_5,
    calc_metrics_step_4_of_5,
    calc_metrics_step_5_of_5,
    get_create_results_folder_fn(results_folder_path),
    save_backtest_result,
    save_metrics_result,
    save_metrics_result_to_pdf,
    create_report_html_fn(strategy_name))