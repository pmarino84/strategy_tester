from backtesting import Strategy
import pytest

from strategy_tester.broker_params import BrokerParamsBuilder
from strategy_tester.backtesting.pipeline.steps import get_add_asset_name, get_add_strategy_name, get_add_telegram_bot, get_add_broker_params
from strategy_tester.pipeline.context import Context
from strategy_tester.pipeline.pipe import pipe

ASSET_NAME = "BTCUSDT"

def test_set_asset_name():
  pipeline = pipe(get_add_asset_name(ASSET_NAME))
  assert pipeline.run().asset_name == ASSET_NAME

STRATEGY_NAME = "Swing Daily"

def test_set_strategy_name():
  pipeline = pipe(get_add_strategy_name(STRATEGY_NAME))
  assert pipeline.run().strategy_name == STRATEGY_NAME

def test_nojobs_error():
  with pytest.raises(Exception):
    pipe().run()

class TheStrategy(Strategy):
  atr_period=10
  atr_multiplier=1.2

def set_strategy(context: Context):
  context.strategy = TheStrategy
  return context

def test_set_strategy():
  pipeline = pipe(set_strategy)

  assert pipeline.run().strategy == TheStrategy

def test_add_telegram_bot():
  pipeline = pipe(get_add_telegram_bot("TELEGRAM_BOT_API_TOKEN", "TELEGRAM_CHAT_ID"))

  context = pipeline.run()

  assert context.telegram_chat_id == "TELEGRAM_CHAT_ID"

def test_add_broker_params():
  broker_params = BrokerParamsBuilder().set_cash(2_000).set_margin(1/30).build()
  pipeline = pipe(get_add_broker_params(broker_params))

  context = pipeline.run()

  assert context.broker_params == broker_params
