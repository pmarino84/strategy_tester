import asyncio
import os
from typing import Optional
from dotenv import dotenv_values
from backtesting import Strategy
import pytest

from ..telegram.bot import TelegramBot
from ..pipeline.context import Context
from ..pipeline.pipe import pipe

ENV = dotenv_values(f"{os.getcwd()}/.env")

ASSET_NAME = "BTCUSDT"

def set_asset_name(context: Context):
  context.asset_name = ASSET_NAME
  return context

def test_set_asset_name():
  pipeline = pipe(set_asset_name)
  assert pipeline.run().asset_name == ASSET_NAME

STRATEGY_NAME = "Swing Daily"

def set_strategy_name(context: Context):
  context.strategy_name = STRATEGY_NAME
  return context

def test_set_strategy_name():
  pipeline = pipe(set_strategy_name)
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

TELEGRAM_CHAT_ID = int(ENV["TELEGRAM_CHAT_ID"])

def get_add_telegram_bot(bot_token: Optional[str] = None, chat_id: Optional[str] = None):
  def add_telegram_bot(context: Context):
    if bot_token and chat_id:
      context.telegram_chat_id = chat_id
      context.telegram_bot = TelegramBot(bot_token)
    return context
  return add_telegram_bot

def test_add_telegram_bot():
  pipeline = pipe(get_add_telegram_bot(ENV["TELEGRAM_BOT_API_TOKEN"], TELEGRAM_CHAT_ID))

  context = pipeline.run()

  assert context.telegram_chat_id == TELEGRAM_CHAT_ID
