import os
from dotenv import dotenv_values

from ....strategy_tester.broker_params import BrokerParamsBuilder
from .pipeline import create_pipeline_backtest

# to execute the script past this code in the terminal:
# python3 -m src.examples.single_asset.two_ema_cross.backtest

ENV = dotenv_values(f"{os.getcwd()}/.env")

ASSET_NAME = "GOOG"

print(f"Creating pipeline for asset {ASSET_NAME}...")
pipeline = create_pipeline_backtest(
  f"{os.getcwd()}/src/examples/single_asset/two_ema_cross/results/GOOG/backtest",
  asset_name=ASSET_NAME,
  strategy_name="Two EMA Cross Swing",
  broker_params=BrokerParamsBuilder().set_cash(10_000).set_commission(0.002).set_exclusive_orders(True).build(),
  telegram_bot_token=ENV["TELEGRAM_BOT_API_TOKEN"],
  telegram_chat_id=int(ENV["TELEGRAM_CHAT_ID"]))
print(f"Running the pipeline for asset {ASSET_NAME}...")
pipeline.run()