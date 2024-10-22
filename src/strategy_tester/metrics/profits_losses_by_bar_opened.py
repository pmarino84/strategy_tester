import pandas as pd

def get_profits_by_time_opened(trades_data: pd.DataFrame) -> pd.DataFrame:
  """
  Calculate the profits by time opened as pandas DataFrame.

  `trades_data` is the trades table from backtesting/optimization statistics result

  Return a `pd.DataFrame` with two columns:\n
  + PnL      : the aggregated profits\n
  + BarsCount: the bars opened count for the profits\n
  """
  if trades_data.empty:
    return pd.DataFrame()

  return trades_data[trades_data["PnL"] > 0][["PnL", "BarsCount"]]

def get_losses_by_time_opened(trades_data: pd.DataFrame) -> pd.DataFrame:
  """
  Calculate the losses by time opened as pandas DataFrame.

  `trades_data` is the trades table from backtesting/optimization statistics result

  Return a `pd.DataFrame` with two columns:\n
  + PnL      : the aggregated losses\n
  + BarsCount: the bars opened count for the losses\n
  """
  if trades_data.empty:
    return pd.DataFrame()
  
  return trades_data[trades_data["PnL"] < 0][["PnL", "BarsCount"]]