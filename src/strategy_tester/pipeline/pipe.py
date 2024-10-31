import asyncio
import traceback
from typing import Callable

from ..utils.log import log
from .context import Context


class Pipeline:
  """
  Run the given jobs sequentially.\n\n

  `jobs` Job sequence. It's a function that take the context as input, save it's result inside the context and return the context for the next job e.g.:\n

  ```python
  def my_job(context: strategy_tester.pipeline.context.Context):\n
    # your job code go here, save it's result inside the context\n
    return context
  ```
  """
  _jobs: list[Callable[[Context], Context]]
  
  def __init__(self, jobs: list[Callable[[Context], Context]]) -> None:
    self._jobs = jobs

  def run(self, context: Context):
    """
    Execute the jobs sequence.
    Return the resulting context.
    """
    
    for job in self._jobs:
      try:
        log(f"Running job {job.__name__}", context.strategy_name, context.asset_name)
        context = job(context)
      except Exception as ex:
        traceback.print_exc()
        if context.telegram_bot:
          stack_trace = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
          asset_name = context.asset_name or "N/A"
          strategy_name = context.strategy_name or context.strategy.__name__
          message = f"Failed to test strategy {strategy_name} with asset {asset_name} Error:\n {stack_trace}"
          log(f"Send notification error for asset {asset_name} to chat id `{context.telegram_chat_id}`", context.strategy_name, context.asset_name)
          try:
            async def notify():
              await context.telegram_bot.send_message(context.telegram_chat_id, message)
            asyncio.run(notify())
          except:
            log(f"Can't send error messaget to Telegram chat", "ERROR", context.strategy_name, context.asset_name)
            traceback.print_exc()
        break
    return context
