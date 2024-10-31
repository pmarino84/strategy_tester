import pytest
from backtesting import Strategy

from strategy_tester.backtesting.broker_params import BrokerParamsBuilder
from strategy_tester.backtesting.pipeline.steps import *
from strategy_tester.pipeline.context import Context
from strategy_tester.pipeline.pipe import Pipeline

class TheStrategy(Strategy):
  atr_period=10
  atr_multiplier=1.2

def set_strategy(context: Context):
  context.strategy = TheStrategy
  return context

def test_set_strategy():
  pipeline = Pipeline([set_strategy])

  assert pipeline.run().strategy == TheStrategy

def test_add_telegram_bot():
  pipeline = Pipeline([get_add_telegram_bot_job("TELEGRAM_BOT_API_TOKEN", "TELEGRAM_CHAT_ID")])

  context = pipeline.run()

  assert context.telegram_chat_id == "TELEGRAM_CHAT_ID"

def test_add_broker_params():
  broker_params = BrokerParamsBuilder().set_cash(2_000).set_margin(1/30).build()
  pipeline = Pipeline([get_add_broker_params_job(broker_params)])

  context = pipeline.run()

  assert context.broker_params == broker_params
