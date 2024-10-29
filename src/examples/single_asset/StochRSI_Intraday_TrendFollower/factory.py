from ....strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from ....strategy_tester.backtesting.pipeline.steps import *
from ....strategy_tester.pipeline.pipe import Pipeline, pipe
from ....strategy_tester.pipeline.context import Context

def get_add_fraction_unit(fraction_unit: float):
  def add_fraction_unit(context: Context):
    context.custom["fraction_unit"] = fraction_unit
    return context
  return add_fraction_unit

def process_data_with_fraction_unit(context: Context):
  fraction_unit = context.custom["fraction_unit"]
  context.data = (context.data / fraction_unit).assign(Volume=context.data["Volume"] * fraction_unit)
  return context

def process_trades_with_fraction_unit(context: Context):
  fraction_unit = context.custom["fraction_unit"]
  trades = context.custom["trades"]
  trades["EntryPrice"] *= fraction_unit
  trades["ExitPrice"] *= fraction_unit
  trades["Size"]/= fraction_unit
  return context

def create_backtest_pipeline_with_metrics_and_fractional_units(load_data,
                                                               create_strategy,
                                                               results_folder_path,
                                                               fraction_unit: float = 1.0,
                                                               asset_name: str = None,
                                                               strategy_name: str = None,
                                                               broker_params: BrokerParams = BrokerParamsBuilder().build(),
                                                               telegram_bot_token: str = None,
                                                               telegram_chat_id: str = None) -> Pipeline:
  return pipe(
    add_start_time,
    get_add_asset_name(asset_name),
    get_add_strategy_name(strategy_name),
    get_add_broker_params(broker_params),
    get_add_telegram_bot(telegram_bot_token, telegram_chat_id),
    get_add_fraction_unit(fraction_unit),
    load_data,
    process_data_with_fraction_unit,
    create_strategy,
    strategy_backtest,
    check_trades_available,
    copy_trades_table,
    process_trades_with_fraction_unit,
    calc_metrics_step_1_of_5,
    calc_metrics_step_2_of_5,
    calc_metrics_step_3_of_5,
    calc_metrics_step_4_of_5,
    calc_metrics_step_5_of_5,
    get_create_results_folder_fn(results_folder_path),
    save_report_to_pdf,
    add_end_time,
    send_report_to_telegram_chat)