import pandas as pd
from .utils import assert_offset_values, resample_offset_to_field_name

def _get_entries_counts_bars(data_pnl: pd.Series, offset: str):
  if data_pnl.empty:
    return pd.DataFrame({
    "entries_profits": [],
    "entries_losses": [],
  })

  assert_offset_values(offset)
  
  field_name = resample_offset_to_field_name(offset)
  entries_losses = data_pnl[data_pnl < 0].apply(lambda x: -abs(x/x)).resample(offset).sum()
  entries_losses = pd.DataFrame(entries_losses)
  if field_name == "hour":
    entries_losses[field_name] = entries_losses.index.map(lambda x: x.hour)
  elif field_name == "day_of_week":
    entries_losses[field_name] = entries_losses.index.map(lambda x: x.dayofweek)
  else:
    entries_losses[field_name] = entries_losses.index.map(lambda x: x.month)
  entries_losses = entries_losses.groupby([field_name]).sum()["PnL"]

  entries_profits = data_pnl[data_pnl > 0].apply(lambda x: abs(x/x)).resample(offset).sum()
  entries_profits = pd.DataFrame(entries_profits)
  if field_name == "hour":
    entries_profits[field_name] = entries_profits.index.map(lambda x: x.hour)
  elif field_name == "day_of_week":
    entries_profits[field_name] = entries_profits.index.map(lambda x: x.dayofweek)
  else:
    entries_profits[field_name] = entries_profits.index.map(lambda x: x.month)
  entries_profits = entries_profits.groupby([field_name]).sum()["PnL"]

  unified = pd.DataFrame({
    "entries_profits": entries_profits.values,
    "entries_losses": abs(entries_losses.values),
  }, index=entries_profits.index)

  return unified

def get_entries_by_hour(data_pnl: pd.Series):
  return _get_entries_counts_bars(data_pnl, "H")

def get_entries_by_dayofweek(data_pnl: pd.Series):
  return _get_entries_counts_bars(data_pnl, "D")

def get_entries_by_month(data_pnl: pd.Series):
  return _get_entries_counts_bars(data_pnl, "M")
