import pandas as pd

from ....utils.parsers import parse_data_for_json


def _statistics_to_json(stats: pd.Series, pnl: pd.Series):
  result = {}
  for i in range(len(stats.index)):
    key = stats.index[i]
    if not key.startswith("_"):
      result[key] = parse_data_for_json(stats.values[i])
  
  if pnl.empty:
    return result
  
  profits = pnl[pnl > 0]
  losses = pnl[pnl < 0]
  profit_min = profits.min()
  profit_max = profits.max()
  profit_avg = profits.sum() / len(profits)
  loss_min = losses.max() # I use max function because losses are negative values, same reasoning for losses_max
  loss_max = losses.min()
  loss_avg = losses.sum() / len(losses)
  profits_less_then_10_count = len(profits[profits < 10])

  result["Min. Profit"] = profit_min
  result["Max. Profit"] = profit_max
  result["Avg. Profit"] = profit_avg

  result["Min. Loss"] = loss_min
  result["Max. Loss"] = loss_max
  result["Avg. Loss"] = loss_avg

  result["Profit less then 10 USD count"] = profits_less_then_10_count

  return result
