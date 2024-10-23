import os

from dotenv import dotenv_values

from ....strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from ....strategy_tester.backtesting.optimization_params import OptimizationParamsBuilder
from .assets import assets
from .pipeline import create_pipeline

# python3 -m src.examples.multi_asset.bollinger_bands_swing.optimization

ENV = dotenv_values(f"{os.getcwd()}/.env")

STRATEGY_NAME = "Bollinger Bands Swing"

BROKER_PARAMS = BrokerParamsBuilder().set_cash(2_000).set_margin(1/30).set_exclusive_orders(True).build()
OPTIMIZATION_PARAMS = OptimizationParamsBuilder().set_maximize("Return [%]").set_max_tries(300).build()

for asset_name in assets:
  print(f"Creating pipeline for asset {asset_name}...")
  pipeline = create_pipeline(
    asset_name,
    assets[asset_name],
    STRATEGY_NAME,
    BROKER_PARAMS,
    OPTIMIZATION_PARAMS,
    ENV["TELEGRAM_BOT_API_TOKEN"],
    int(ENV["TELEGRAM_CHAT_ID"]))
  print(f"Running the pipeline for asset {asset_name}...")
  pipeline.run()