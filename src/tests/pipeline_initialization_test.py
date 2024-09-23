import asyncio
import os
from typing import Optional
from backtesting import Strategy
from dotenv import dotenv_values

from ..telegram.bot import TelegramBot
from ..pipeline.context import Context
from ..pipeline.pipe import pipe

# run the test with the command:
# python3 -m src.tests.pipeline_initialization_test

ENV = dotenv_values(f"{os.getcwd()}/.env")

def set_asset_name(context: Context):
  context.asset_name = "BTCUSDT"
  return context

def get_add_telegram_bot(bot_token: Optional[str] = None, chat_id: Optional[str] = None):
  def add_telegram_bot(context: Context):
    if bot_token and chat_id:
      context.telegram_chat_id = chat_id
      context.telegram_bot = TelegramBot(bot_token)
    return context
  return add_telegram_bot

def create_strategy(context: Context):
  class TheStrategy(Strategy):
    atr_period=10
    atr_multiplier=1.2
  
  context.strategy = TheStrategy
  return context


def send_notification_to_telegram_chat(context: Context):
  if context.telegram_bot:
    asset_name = context.asset_name or "N/A"
    strategy_name = context.strategy_name or context.strategy.__name__
    print(f"Sending notification for asset {asset_name} to chat id `{context.telegram_chat_id}`...")
    # https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues
    async def notify():
      await context.telegram_bot.send_message(context.telegram_chat_id, f"[TEST] {asset_name} {strategy_name}")
    asyncio.run(notify())

# pipeline = pipe(get_add_telegram_bot(), create_strategy)
# pipeline = pipe(get_add_telegram_bot(ENV["TELEGRAM_BOT_API_TOKEN"]), create_strategy)
pipeline = pipe(
  set_asset_name,
  get_add_telegram_bot(ENV["TELEGRAM_BOT_API_TOKEN"], int(ENV["TELEGRAM_CHAT_ID"])),
  create_strategy,
  send_notification_to_telegram_chat)

context = pipeline.run()
print(context)
