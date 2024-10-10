import pandas as pd

from ....utils import flatten_list


def _dataframe_to_grouped_barchart_options(data: pd.DataFrame, title: str = None):
  if data.empty:
    return None
  
  x_values = data.index.map(lambda x: str(x)).to_list()
  series = []

  for key in data.columns:
    df = data[[key]]
    series.append({
      "type": "bar",
      "name": key,
      "data": flatten_list(df.values.tolist())
    })

  options = {
    "animation": False,
    "tooltip": {},
    "xAxis": {
      "data": x_values,
    },
    "yAxis": {},
    "legend": {
      "right": 50,
    },
    "series": series
  }

  if title:
    options["title"] = { "text": title }
  
  return options
