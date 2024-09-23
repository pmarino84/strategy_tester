
# TODO: con le metriche profits/losses by time opened provare a mostrare il timedelta
# TODO: sistemare le funzioni che salvano i report in pdf/html nel caso non ci siano profitti/perdite si rompe tutto
from ...backtesting.pipeline.steps import *
from ...broker import BrokerParams, BrokerParamsBuilder
from ...pipeline.pipe import pipe

# TODO: save report to pdf and html without metrics
def create_backtest_pipeline(load_data,
                             create_strategy,
                             results_folder_path,
                             asset_name: str = None,
                             strategy_name: str = None,
                             broker_params: BrokerParams = BrokerParamsBuilder().build(),
                             telegram_bot_token: str = None,
                             telegram_chat_id: str = None):
  return pipe(
    load_data,
    create_strategy,
    get_add_asset_name(asset_name),
    get_add_strategy_name(strategy_name),
    get_add_broker_params(broker_params),
    get_add_telegram_bot(telegram_bot_token, telegram_chat_id),
    strategy_backtest,
    copy_trades_table,
    get_create_results_folder_fn(results_folder_path),
    save_backtest_result,
    send_report_to_telegram_chat)

# TODO: con le metriche profits/losses by time opened provare a mostrare il timedelta
# TODO: sistemare le funzioni che salvano i report in pdf/html nel caso non ci siano profitti/perdite si rompe tutto
def create_backtest_pipeline_with_metrics(load_data,
                                          create_strategy,
                                          results_folder_path,
                                          asset_name: str = None,
                                          strategy_name: str = None,
                                          broker_params: BrokerParams = BrokerParamsBuilder().build(),
                                          telegram_bot_token: str = None,
                                          telegram_chat_id: str = None):
  return pipe(
    load_data,
    create_strategy,
    get_add_asset_name(asset_name),
    get_add_strategy_name(strategy_name),
    get_add_broker_params(broker_params),
    get_add_telegram_bot(telegram_bot_token, telegram_chat_id),
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
    get_report_html_fn(strategy_name),
    send_report_to_telegram_chat)