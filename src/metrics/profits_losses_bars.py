import pandas as pd
from .utils import _assert_offset_values, _resample_offset_to_field_name

def _get_profits_losses_bars(data_pnl: pd.Series, offset: str):
  _assert_offset_values(offset)
  field_name = _resample_offset_to_field_name(offset)
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
  return _get_profits_losses_bars(data_pnl, "H")

def get_profits_losses_by_dayofweek(data_pnl: pd.Series):
  return _get_profits_losses_bars(data_pnl, "D")

def get_profits_losses_by_month(data_pnl: pd.Series):
  return _get_profits_losses_bars(data_pnl, "M")
