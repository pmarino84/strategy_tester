import asyncio
import traceback
from .context import Context

class Pipeline:
  """
  Run the given jobs sequentially.\n\n
  A job is a function that take the context as input, save it's result inside the context and return it for the next job e.g.:\n

    def my_job(context: `strategy_tester.pipeline.Context`):\n
      # your job code go here, save it's result inside the context\n
      return context
  """
  def __init__(self, jobs) -> None:
    self.jobs = jobs
    """jobs sequence"""

  def run(self):
    context = Context()
    
    for job in self.jobs:
      try:
        print(f"Running job {job.__name__}...")
        context = job(context)
      except Exception as ex:
        traceback.print_exc()
        if context.telegram_bot:
          stack_trace = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
          asset_name = context.asset_name or "N/A"
          strategy_name = context.strategy_name or context.strategy.__name__
          message = f"Failed to test strategy {strategy_name} with asset {asset_name} Error:\n {stack_trace}"
          print(f"Send notification error for asset {asset_name} to chat id `{context.telegram_chat_id}`")
          try:
            async def notify():
              await context.telegram_bot.send_message(context.telegram_chat_id, message)
            asyncio.run(notify())
          except:
            print("Can't send error messaget to Telegram chat")
            traceback.print_exc()
        break
    return context

def pipe(*jobs):
  """
  Return the pipeline instance to manage the given jobs sequence
  """
  assert len(jobs) > 0, "Should pass a job list"
    
  return Pipeline(jobs)