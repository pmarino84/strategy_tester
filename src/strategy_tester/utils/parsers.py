import pandas as pd


def parse_data_for_json(x):
  if isinstance(x, pd.Timestamp) or isinstance(x, pd.Timedelta):
    return str(x)
  return x
