import math
from itertools import combinations

import matplotlib as mpl
import pandas as pd

_viridis_cmap = mpl.colormaps["viridis"]
# x = np.linspace(0.0, 1.0, 100)
# rgb = viridis_cmap(x)[np.newaxis, :, :3]
# print(rgb)
_viridis_cmap_hex_colors = []
for i in range(_viridis_cmap.N):
  rgba = _viridis_cmap(i)
  _viridis_cmap_hex_colors.append(mpl.colors.rgb2hex(rgba))

def _dataframe_to_heatmapchart_options(df: pd.DataFrame):
  first_name, second_name = df.index.names
  first_levels = df.index.levels[0].to_list()
  second_levels = df.index.levels[1].to_list()

  df_1 = df.unstack()
  df_1.columns = df_1.columns.droplevel()

  values = df_1.values.T.tolist()
  # values = df_1.values.tolist()

  data = []
  r = 0
  max_value = 0
  for row in values:
    c = 0
    for value in row:
      formatted_value = '-' if math.isnan(value) else round(value, 2)
      data.append([ r, c, formatted_value ])
      if value > max_value:
        max_value = value
      c = c + 1
    r = r + 1
  
  series = [
    {
      "name": f"{first_name} x {second_name} heatmap",
      "type": "heatmap",
      "data": data,
      "label": { "show": True }
    }
  ]

  title = f"{first_name} x {second_name}"

  options = {
    "title": { "text": title },
    "animation": False,
    "tooltip": {},
    # "grid": {
    #   "height": '50%',
    #   "top": '10%'
    # },
    "xAxis": {
      "type": "category",
      "name": second_name,
      "nameLocation": "center",
      "nameGap": 30,
      "data": second_levels,
      "splitArea": { "show": True }
    },
    "yAxis": {
      "type": "category",
      "name": first_name,
      "nameLocation": "center",
      "nameGap": 30,
      "data": first_levels,
      "splitArea": { "show": True }
    },
    "visualMap": {
      "show": False,
      "min": 0,
      "max": math.ceil(max_value),
      "calculable": True,
      "orient": 'horizontal',
      "left": 'center',
      "bottom": '15%',
      "inRange": {
        "color": _viridis_cmap_hex_colors
      }
    },
    "series": series
  }
  return options

def _parse_heatmap_series(heatmap: pd.Series):
  if not isinstance(heatmap, pd.Series) or heatmap.empty:
    return None
  
  params_combinations = combinations(heatmap.index.names, 2)
  dataframes = [heatmap.groupby(list(dimensions)).agg("mean").to_frame(name="_Value") for dimensions in params_combinations]

  options = [_dataframe_to_heatmapchart_options(df) for df in dataframes]
  return options
