import pandas as pd


def _dataframe_to_scatterchart_cartesian_options(data: pd.DataFrame, columns, title: str = None):
  if data.empty:
    return None
  
  series = [{ "type": "scatter", "data": data[columns].values.tolist() }]
  options = {
    "animation": False,
    "tooltip": {},
    "xAxis": {},
    "yAxis": {},
    "series": series
  }

  if title:
    options["title"] = { "text": title }

  return options