
# TODO: con le metriche profits/losses by time opened provare a mostrare il timedelta
from typing import Callable

from ...backtesting.pipeline.steps import *
from ...pipeline import Context, Pipeline
from ..broker_params import BrokerParams, BrokerParamsBuilder


def create_backtest_jobs(
  load_data,
  create_strategy,
  results_folder_path,
  broker_params: BrokerParams = BrokerParamsBuilder().build(),
  telegram_bot_token: str = None,
  telegram_chat_id: str = None) -> list[Callable[[Context], Context]]:
  """
  Return the default basic jobs to backtest a strategy.

  `load_data` custom function to load data needed to backtest the strategy.
  `create_strategy` custom function that return your Strategy class.
  `results_folder_path` the folder where you want to store the result files.
  `asset_name` asset used for backtest the strategy (e.g. EURUSD, BTCUSDT).
  `strategy_name` strategy name.
  `broker_params` params for the broker.
  `telegram_bot_token` (optional) Telegram bot token, don't pass it if you don't want to send notification over Telegram.
  `telegram_chat_id` (optional) Telegram chat id, don't pass it if you don't want to send notification over Telegram.

  Jobs:
  + add the broker params to the context\n
  + add the telegram bot info (if given)\n
  + load data with the given custom functions\n
  + create the strategy class with the given custom functions\n
  + backtest the strategy\n
  + copy the trades table from the result statistics into the context to simplify the metrics calculation\n
  + create the result folder\n
  + save the strategy params as text file\n
  + save the broker params as text file\n
  + save the backtest result on files\n
  + send the notification to telegram\n
  """
  return [
    add_start_time,
    get_add_broker_params_job(broker_params),
    get_add_telegram_bot_job(telegram_bot_token, telegram_chat_id),
    load_data,
    create_strategy,
    strategy_backtest,
    copy_trades_table,
    get_create_results_folder_job(results_folder_path),
    save_data,
    save_report_to_pdf,
    add_end_time,
    send_report_to_telegram_chat,
  ]

def create_backtest_pipeline(
  load_data,
  create_strategy,
  results_folder_path,
  broker_params: BrokerParams,
  telegram_bot_token: str,
  telegram_chat_id: str) -> Pipeline:
  """
  Return the default basic pipeline to backtest a strategy.

  For the arguments see `.create_backtest_jobs`
  """
  return Pipeline(create_backtest_jobs(
    load_data,
    create_strategy,
    results_folder_path,
    broker_params,
    telegram_bot_token,
    telegram_chat_id,
  ))

# TODO: con le metriche profits/losses by time opened provare a mostrare il timedelta
def create_backtest_jobs_with_metrics(
  load_data,
  create_strategy,
  results_folder_path,
  broker_params: BrokerParams = BrokerParamsBuilder().build(),
  telegram_bot_token: str = None,
  telegram_chat_id: str = None) -> list[Callable[[Context], Context]]:
  """
  Return the default basic jobs added with metrics calculation to backtest a strategy.

  `load_data` custom function to load data needed to backtest the strategy.
  `create_strategy` custom function that return your Strategy class.
  `results_folder_path` the folder where you want to store the result files.
  `asset_name` asset used for backtest the strategy (e.g. EURUSD, BTCUSDT).
  `strategy_name` strategy name.
  `broker_params` params for the broker.
  `telegram_bot_token` (optional) Telegram bot token, don't pass it if you don't want to send notification over Telegram.
  `telegram_chat_id` (optional) Telegram chat id, don't pass it if you don't want to send notification over Telegram.

  Jobs:
  + add the broker params to the context\n
  + add the telegram bot info (if given)\n
  + load data with the given custom functions\n
  + create the strategy class with the given custom functions\n
  + backtest the strategy\n
  + check if there is a trade list\n
  + copy the trades table from the result statistics into the context to simplify the metrics calculation\n
  + calculate the metrics with various steps\n
  + create the result folder\n
  + save the strategy params as text file\n
  + save the broker params as text file\n
  + save the backtest result on files\n
  + save the metrics on files\n
  + save the metrics as pdf report\n
  + save the html report\n
  + send the notification to telegram\n
  """
  return [
    add_start_time,
    get_add_broker_params_job(broker_params),
    get_add_telegram_bot_job(telegram_bot_token, telegram_chat_id),
    load_data,
    create_strategy,
    strategy_backtest,
    check_trades_available,
    copy_trades_table,
    calc_metrics_step_1_of_5,
    calc_metrics_step_2_of_5,
    calc_metrics_step_3_of_5,
    calc_metrics_step_4_of_5,
    calc_metrics_step_5_of_5,
    get_create_results_folder_job(results_folder_path),
    save_data,
    save_report_to_pdf,
    add_end_time,
    send_report_to_telegram_chat,
  ]

def create_backtest_pipeline_with_metrics(
  load_data,
  create_strategy,
  results_folder_path,
  broker_params: BrokerParams,
  telegram_bot_token: str,
  telegram_chat_id: str) -> Pipeline:
  """
  Return the default basic pipeline added with metrics calculation to backtest a strategy.

  For the arguments see `.create_backtest_jobs_with_metrics`
  """
  return Pipeline(create_backtest_jobs_with_metrics(
    load_data,
    create_strategy,
    results_folder_path,
    broker_params,
    telegram_bot_token,
    telegram_chat_id
  ))