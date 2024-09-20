import pandas as pd

def get_profits_by_time_opened(trades_data: pd.DataFrame):
  data = trades_data[trades_data["PnL"] > 0][["PnL", "BarsCount"]]
  return data

def get_losses_by_time_opened(trades_data: pd.DataFrame):
  data = trades_data[trades_data["PnL"] < 0][["PnL", "BarsCount"]]
  return data