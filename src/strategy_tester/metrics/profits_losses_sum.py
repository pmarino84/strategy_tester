import pandas as pd

from .utils import assert_offset_values, resample_offset_to_field_name


def _get_profits_losses_sum_bars(data_pnl: pd.Series, offset: str) -> pd.Series:
  if data_pnl.empty:
    return pd.Series()
  
  assert_offset_values(offset)
  
  field_name = resample_offset_to_field_name(offset)
  data = data_pnl.resample(offset).sum()
  data = pd.DataFrame(data)
  if field_name == "hour":
    data[field_name] = data.index.map(lambda x: x.hour)
  elif field_name == "day_of_week":
    data[field_name] = data.index.map(lambda x: x.dayofweek)
  else:
    data[field_name] = data.index.map(lambda x: x.month)
  data = data.groupby([field_name]).sum()["PnL"]

  return data

def get_profits_losses_sum_by_hour(data_pnl: pd.Series) -> pd.Series:
  """
  Calculate the sum of profits and losses by hour as pandas Series.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result
  """
  return _get_profits_losses_sum_bars(data_pnl, "H")

def get_profits_losses_sum_by_dayofweek(data_pnl: pd.Series) -> pd.Series:
  """
  Calculate the sum of profits and losses by day of week as pandas Series.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result
  """
  return _get_profits_losses_sum_bars(data_pnl, "D")

def get_profits_losses_sum_by_month(data_pnl: pd.Series) -> pd.Series:
  """
  Calculate the sum of profits and losses by month as pandas Series.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result
  """
  return _get_profits_losses_sum_bars(data_pnl, "M")
