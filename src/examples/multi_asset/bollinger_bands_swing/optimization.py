import multiprocessing as mp
import os

import numpy as np
from dotenv import dotenv_values

from ....strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from ....strategy_tester.backtesting.optimization_params import OptimizationParamsBuilder
from .assets import assets
from .pipeline import create_pipeline

# use the following command to run the example:
# python3 -m src.examples.multi_asset.bollinger_bands_swing.optimization

ENV = dotenv_values(f"{os.getcwd()}/.env")

STRATEGY_NAME = "Bollinger Bands Swing"

BROKER_PARAMS = BrokerParamsBuilder().set_cash(2_000).set_margin(1/30).set_exclusive_orders(True).build()
OPTIMIZATION_PARAMS = OptimizationParamsBuilder().set_maximize("Return [%]").set_max_tries(300).build()

def run(assets) -> None:
  for asset in assets:
    asset_name = asset[0]
    asset_data = asset[1]
    print(f"[{STRATEGY_NAME}][{asset_name}] Creating pipeline...")
    pipeline = create_pipeline(
      asset_name,
      asset_data,
      STRATEGY_NAME,
      BROKER_PARAMS,
      OPTIMIZATION_PARAMS,
      ENV["TELEGRAM_BOT_API_TOKEN"],
      int(ENV["TELEGRAM_CHAT_ID"]))
    print(f"[{STRATEGY_NAME}][{asset_name}] Running the pipeline...")
    pipeline.run()

asset_list = list(assets.items())
if __name__ == "__main__":
  chunks = np.array_split(asset_list, mp.cpu_count())

  for i in reversed(range(len(chunks))):
    if len(chunks[i]) == 0:
      chunks.pop(i)
  
  pool = []
  for i in range(len(chunks)):
    process = mp.Process(target=run, args=(chunks[i].tolist(),))
    pool.append(process)
    process.start()
  for process in pool:
    process.join()
