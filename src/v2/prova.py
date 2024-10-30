import time
from typing import Callable, Optional

import pandas as pd


class Context:
  start_time: time.time   # TODO: sostituire con datetime
  end_time: time.time     # TODO: sostituire con datetime
  elapsed_time: time.time # TODO: sostituire con timedelta
  asset_name: Optional[str]
  strategy_name: Optional[str]
  data: Optional[pd.DataFrame]
  
  def __init__(self) -> None:
    # self.reset_v1()
    self.reset_v2()
  
  def reset_v1(self) -> None:
    self.start_time    = 0
    self.end_time      = 0
    self.elapsed_time  = 0
    self.asset_name    = "N/A"
    self.strategy_name = "N/A"
  
  def reset_v2(self) -> None:
    self.start_time    = 0
    self.end_time      = 0
    self.elapsed_time  = 0
    self.asset_name    = None
    self.strategy_name = None
  
  def __repr__(self) -> str:
    result = "Context:"
    result += f"\n+ Asset name   : {self.asset_name}"
    result += f"\n+ Strategy name: {self.strategy_name}"
    result += f"\n+ Start time   : {self.start_time}"
    result += f"\n+ End time     : {self.end_time}"
    result += f"\n+ Elapsed time : {self.elapsed_time}"
    return result

class Pipeline:
  _jobs: list[Callable[[Context], Context]]

  def __init__(self, jobs: list[Callable[[Context], Context]] = []) -> None:
    self._jobs = jobs
  
  def run(self, context: Context):
    for job in self._jobs:
      print(f"Running job {job.__name__}")
      context = job(context)
    return context
















context = Context()
context.asset_name    = "FX:EURUSD"
context.strategy_name = "BB Bounce"

def set_start_time(context: Context):
  context.start_time = time.time()
  return context

def job_1(context: Context):
  return context

def job_2(context: Context):
  return context

def job_3(context: Context):
  return context

def set_end_time(context: Context):
  context.end_time = time.time()
  return context

def set_elapsed_time(context: Context):
  context.elapsed_time = context.end_time - context.start_time
  return context

pipeline = Pipeline([set_end_time, job_1, job_2, job_3, set_end_time, set_elapsed_time])

context = pipeline.run(context)
print(context)
