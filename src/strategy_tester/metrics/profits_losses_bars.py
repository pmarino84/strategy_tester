import pandas as pd
from .utils import assert_offset_values, resample_offset_to_field_name

def _get_profits_losses_bars(data_pnl: pd.Series, offset: str):
  if data_pnl.empty:
    return pd.DataFrame({
    "profits": [],
    "losses": [],
  })

  assert_offset_values(offset)
  
  field_name = resample_offset_to_field_name(offset)
  losses = data_pnl[data_pnl < 0].resample(offset).sum()
  losses = pd.DataFrame(losses)
  if field_name == "hour":
    losses[field_name] = losses.index.map(lambda x: x.hour)
  elif field_name == "day_of_week":
    losses[field_name] = losses.index.map(lambda x: x.dayofweek)
  else:
    losses[field_name] = losses.index.map(lambda x: x.month)
  losses = losses.groupby([field_name]).sum()["PnL"]

  profits = data_pnl[data_pnl > 0].resample(offset).sum()
  profits = pd.DataFrame(profits)
  if field_name == "hour":
    profits[field_name] = profits.index.map(lambda x: x.hour)
  elif field_name == "day_of_week":
    profits[field_name] = profits.index.map(lambda x: x.dayofweek)
  else:
    profits[field_name] = profits.index.map(lambda x: x.month)
  profits = profits.groupby([field_name]).sum()["PnL"]

  unified = pd.DataFrame({
    "profits": profits.values,
    "losses": abs(losses.values),
  }, index=profits.index)

  return unified

def get_profits_losses_by_hour(data_pnl: pd.Series):
  """
  Aggregate profits/losses by hour as pandas DataFrame.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result

  Return a `pd.DataFrame` with two columns:\n
  + profits: the aggregated profits\n
  + losses : the aggregated losses\n
  """
  return _get_profits_losses_bars(data_pnl, "H")

def get_profits_losses_by_dayofweek(data_pnl: pd.Series):
  """
  Aggregate profits/losses by day of week as pandas DataFrame.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result

  Return a `pd.DataFrame` with two columns:\n
  + profits: the aggregated profits\n
  + losses : the aggregated losses\n
  """
  return _get_profits_losses_bars(data_pnl, "D")

def get_profits_losses_by_month(data_pnl: pd.Series):
  """
  Aggregate profits/losses by month as pandas DataFrame.

  `data_pnl` is the trades PnL (Profits Net Loss) from backtesting/optimization statistics result

  Return a `pd.DataFrame` with two columns:\n
  + profits: the aggregated profits\n
  + losses : the aggregated losses\n
  """
  return _get_profits_losses_bars(data_pnl, "M")
