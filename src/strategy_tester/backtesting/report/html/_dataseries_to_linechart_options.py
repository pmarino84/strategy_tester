import pandas as pd


def _dataseries_to_linechart_options(data: pd.Series, title: str = None):
  if data.empty:
    return None
  
  x_values = data.index.map(lambda x: str(x)).to_list()
  series = [{ "type": "line", "data": data.values.tolist() }]
  options = {
    "animation": False,
    "tooltip": {},
    "xAxis": {
      "data": x_values,
    },
    "yAxis": {},
    "legend": {},
    "series": series
  }

  if title:
    options["title"] = { "text": title }

  return options
