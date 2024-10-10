import pandas as pd

from ....utils import parse_data_for_json


def _trades_to_json(data: pd.DataFrame):
  if data.empty:
    return None
  
  result = {}

  for key in data.columns:
    df = data[key].map(parse_data_for_json)
    result[key] = df.values.tolist()

  return result