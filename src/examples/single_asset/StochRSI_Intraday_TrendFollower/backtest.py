import os

from dotenv import dotenv_values

from ....strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from ....strategy_tester.pipeline import Context
from ....strategy_tester.utils.log import log
from .pipeline import create_backtest_pipeline

# to execute the script past this code in the terminal:
# python3 -m src.examples.single_asset.StochRSI_Intraday_TrendFollower.backtest

ENV = dotenv_values(f"{os.getcwd()}/.env")

STRATEGY_NAME = "Stochastic RSI Scalp intraday"
ASSET_NAME = "BTCUSDT"

DATA_PARENT_FOLDER = f"{os.getcwd()}/src/examples/data/crypto"
RESULTS_PARENT_FOLDER = f"{os.getcwd()}/src/examples/single_asset/StochRSI_Intraday_TrendFollower"

DATA_FILE_PATH = f"{DATA_PARENT_FOLDER}/BTCUSD_Candlestick_15_M_ASK_05.08.2019-29.04.2022.csv"
RESULTS_FOLDER_PATH = f"{RESULTS_PARENT_FOLDER}/BTCUSDT/results/backtest"

BROKER_PARAMS = BrokerParamsBuilder().set_cash(4_000).set_margin(1/10).build()

log(f"Level='INFO'; Strategy='{STRATEGY_NAME}'; Asset='{ASSET_NAME}' Message='Creating pipeline'", STRATEGY_NAME, ASSET_NAME)

context = Context()
context.asset_name    = ASSET_NAME
context.strategy_name = STRATEGY_NAME

pipeline = create_backtest_pipeline(
  DATA_FILE_PATH,
  "Gmt time",
  "%d.%m.%Y %H:%M:%S",
  RESULTS_FOLDER_PATH,
  broker_params=BROKER_PARAMS,
  telegram_bot_token=ENV["TELEGRAM_BOT_API_TOKEN"],
  telegram_chat_id=int(ENV["TELEGRAM_CHAT_ID"]))

log(f"Level='INFO'; Strategy='{STRATEGY_NAME}'; Asset='{ASSET_NAME}' Message='Running the pipeline'", STRATEGY_NAME, ASSET_NAME)
pipeline.run(context)
