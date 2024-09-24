import pandas as pd

def get_profits_by_time_opened(trades_data: pd.DataFrame):
  if trades_data.empty:
    return pd.DataFrame()

  return trades_data[trades_data["PnL"] > 0][["PnL", "BarsCount"]]

def get_losses_by_time_opened(trades_data: pd.DataFrame):
  if trades_data.empty:
    return pd.DataFrame()
  
  return trades_data[trades_data["PnL"] < 0][["PnL", "BarsCount"]]