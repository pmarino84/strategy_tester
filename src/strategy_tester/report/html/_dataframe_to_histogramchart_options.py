import math

import pandas as pd


# histogram distribution
def _dataframe_to_histogramchart_options(data: pd.Series, bins: int = 10, title: str = None):
  if data.empty:
    return None
  
  min = data.min()
  max = data.max()
  length = max - min + 1
  bin_range = length / bins
  values = [0] * bins
  labels = []

  label_min = min
  label_max = min + bin_range - 1
  for i in range(bins):
    if i > 0:
      label_min = label_max + bin_range
      label_max = label_min + bin_range - 1
    label = f"{round(label_min, 2)}\n{round(label_max, 2)}"
    labels.append(label)

  for val in data.values:
    idx = int(math.floor(val - min) / bin_range)
    values[idx] = values[idx] + 1

  series = [{
    "type": "bar",
    "data": values,
    "barGap": 0,
  }]

  options = {
    "tooltip": {},
    "xAxis"  : {
      "data": labels,
    },
    "yAxis" : {},
    "legend": {},
    "series": series,
  }

  if title:
    options["title"] = { "text": title }
  
  return options
