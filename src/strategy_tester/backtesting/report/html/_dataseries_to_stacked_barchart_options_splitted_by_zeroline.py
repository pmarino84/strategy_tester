import pandas as pd


def _dataseries_to_stacked_barchart_options_splitted_by_zeroline(data: pd.Series, title: str = None):
  if data.empty:
    return None
  
  x_values = data.index.map(lambda x: str(x)).to_list()
  series = []

  positives = data.map(lambda x: x if x > 0 else 0).to_list()
  negatives = data.map(lambda x: x if x < 0 else 0).to_list()

  series.append({
    "type" : "bar",
    "stack": "total",
    "name": "positive",
    "data" : positives,
  })
  series.append({
    "type" : "bar",
    "stack": "total",
    "name": "negative",
    "data" : negatives,
  })

  options = {
    "animation": False,
    "tooltip": {},
    "xAxis"  : {
      "data": x_values,
    },
    "yAxis" : {},
    "legend": {
      "right": 50,
    },
    "series": series
  }

  if title:
    options["title"] = { "text": title }

  return options
