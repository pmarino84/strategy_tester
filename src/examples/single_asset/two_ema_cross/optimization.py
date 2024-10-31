import os

from dotenv import dotenv_values

from ....strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from ....strategy_tester.backtesting.optimization_params import OptimizationParamsBuilder
from ....strategy_tester.pipeline import Context
from ....strategy_tester.utils.log import log
from .pipeline import create_pipeline_optimization

# to execute the script past this code in the terminal:
# python3 -m src.examples.single_asset.two_ema_cross.optimization

ENV = dotenv_values(f"{os.getcwd()}/.env")

ASSET_NAME          = "GOOG"
STRATEGY_NAME       = "Two EMA Cross Swing"
BROKER_PARAMS       = BrokerParamsBuilder().set_cash(10_000).set_commission(0.002).set_exclusive_orders(True).build()
OPTIMIZATION_PARAMS = OptimizationParamsBuilder().set_maximize("Return [%]").set_max_tries(200).set_constraint(lambda p: p.fast_ma_period < p.slow_ma_period).build()

log(f"Creating pipeline for asset {ASSET_NAME}...", STRATEGY_NAME, ASSET_NAME)
context = Context()
context.asset_name    = ASSET_NAME
context.strategy_name = STRATEGY_NAME

pipeline = create_pipeline_optimization(
  f"{os.getcwd()}/src/examples/single_asset/two_ema_cross/results/GOOG/optimization",
  broker_params=BROKER_PARAMS,
  optimization_params=OPTIMIZATION_PARAMS,
  telegram_bot_token=ENV["TELEGRAM_BOT_API_TOKEN"],
  telegram_chat_id=int(ENV["TELEGRAM_CHAT_ID"]))

log(f"Running the pipeline for asset {ASSET_NAME}...", STRATEGY_NAME, ASSET_NAME)
pipeline.run(context)