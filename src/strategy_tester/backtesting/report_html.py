import base64
import json
import math
from itertools import combinations

import pandas as pd
import matplotlib as mpl

from ..pipeline.context import Context

viridis_cmap = mpl.colormaps["viridis"]
# x = np.linspace(0.0, 1.0, 100)
# rgb = viridis_cmap(x)[np.newaxis, :, :3]
# print(rgb)
viridis_cmap_hex_colors = []
for i in range(viridis_cmap.N):
  rgba = viridis_cmap(i)
  viridis_cmap_hex_colors.append(mpl.colors.rgb2hex(rgba))

def flatten_list(matrix):
  flat_list = []
  for row in matrix:
    flat_list += row
  return flat_list

def _dataframe_to_grouped_barchart_options(data: pd.DataFrame, title: str = None):
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

def _dataseries_to_stacked_barchart_options_splitted_by_zeroline(data: pd.Series, title: str = None):
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

def _dataseries_to_linechart_options(data: pd.Series, title: str = None):
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

def _dataframe_to_scatterchart_cartesian_options(data: pd.DataFrame, columns, title: str = None):
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

def _dataframe_to_candlestickchart_options(ohlcv: pd.DataFrame, trades: pd.DataFrame):
  df = ohlcv.copy().reset_index()
  df[df.columns[0]] = df[df.columns[0]].map(lambda x: str(x))
  dataset = df.values.tolist()
  trades_markers = []
  trades_lines = []

  for i, row in trades.iterrows():
    position_size = row["Size"]
    pnl = row["PnL"]
    entry_time = str(row["EntryTime"]) # trades["EntryTime"][i].replace(' ', '\n');
    exit_time = str(row["ExitTime"]) # trades["ExitTime"][i].replace(' ', '\n');
    entry_row = ohlcv[ohlcv.index == entry_time]
    exit_row = ohlcv[ohlcv.index == exit_time]
    entry_marker_price = float((entry_row["Low"] if position_size > 0 else entry_row["High"]).values[0])
    exit_marker_price = float((exit_row["High"] if position_size > 0 else exit_row["Low"]).values[0])
    entry_marker = {
      "name": f"Trade {i}",
      "symbol": "triangle",
      "symbolSize": [20, 30],
      "symbolRotate": 0 if position_size > 0 else 180,
      "coord": [entry_time, entry_marker_price],
      "value": "E",
      "itemStyle": {
        "color": "green" if position_size > 0 else "red"
      }
    }
    exit_marker = {
      "name": f"Trade {i}",
      "symbol": "diamond",
      "symbolSize": [30, 30],
      "symbolRotate": 180 if position_size > 0 else 0,
      "coord": [exit_time, exit_marker_price],
      "value": position_size,
      "itemStyle": {
        "color": "green" if pnl > 0 else "red"
      }
    }
    trades_markers.append(entry_marker)
    trades_markers.append(exit_marker)

    trade_line_entry = {
      "coord": entry_marker["coord"],
      "symbol": "none",
      "value": round(pnl, 2),
      "lineStyle": {
        "color": "green" if pnl > 0 else "red",
        "type": "dashed",
        "dashOffset": 5,
      },
    }
    trade_line_exit = {
      "coord": exit_marker["coord"],
      "symbol": "none",
      "value": round(pnl, 2),
      "lineStyle": {
        "color": "green" if pnl > 0 else "red",
        "type": "dashed",
        "dashOffset": 5,
      },
    }
    trades_lines.append([trade_line_entry, trade_line_exit])

  options = {
    "animation": False,
    "dataset": { "source": dataset },
    "tooltip": {
      "trigger": 'axis',
      "axisPointer": {
        "type": 'line'
      }
    },
    "toolbox": {
      "feature": {
        "dataZoom": {
          "yAxisIndex": False
        }
      }
    },
    "grid": [
      {
        "left"  : '10%',
        "right" : '10%',
        "bottom": 200
      },
      {
        "left"  : '10%',
        "right" : '10%',
        "height": 80,
        "bottom": 80
      }
    ],
    "xAxis": [
      {
        "type"       : 'category',
        "boundaryGap": False,
        "axisLine"   : { "onZero": False },
        "splitLine"  : { "show": False },
        "min"        : 'dataMin',
        "max"        : 'dataMax'
      },
      {
        "type"       : 'category',
        "gridIndex"  : 1,
        "boundaryGap": False,
        "axisLine"   : { "onZero": False },
        "axisTick"   : { "show": False },
        "splitLine"  : { "show": False },
        "axisLabel"  : { "show": False },
        "min"        : 'dataMin',
        "max"        : 'dataMax'
      }
    ],
    "yAxis": [
      {
        "scale"    : True,
        "splitArea": {
          "show": True
        }
      },
      {
        "scale"      : True,
        "gridIndex"  : 1,
        "splitNumber": 2,
        "axisLabel"  : { "show": False },
        "axisLine"   : { "show": False },
        "axisTick"   : { "show": False },
        "splitLine"  : { "show": False }
      }
    ],
    "dataZoom": [
      {
        "type"      : 'inside',
        "xAxisIndex": [0, 1],
        "start"     : 90,
        "end"       : 100
      },
      {
        "show"      : True,
        "xAxisIndex": [0, 1],
        "type"      : 'slider',
        "bottom"    : 10,
        "start"     : 90,
        "end"       : 100
      }
    ],
    "visualMap": {
      "show"       : False,
      "seriesIndex": 1,
      "dimension"  : 6,
      "pieces"     : [
        {
          "value": 1,
          "color": "green"
        },
        {
          "value": -1,
          "color": "red"
        }
      ]
    },
    "series": [
      {
        "type"     : 'candlestick',
        "itemStyle": {
          "color"       : "green",
          "color0"      : "red",
          "borderColor" : "green",
          "borderColor0": "red"
        },
        "encode": {
          "x": 0,
          "y": [1, 4, 3, 2]
        },
        "markPoint": {
          "data"   : trades_markers,
          "tooltip": {},
        },
        "markLine": {
          "symbol": ["none", "none"],
          "data"  : trades_lines,
          "label" : { "position": "middle" }
        },
      },
      {
        "name"      : 'Volume',
        "type"      : 'bar',
        "xAxisIndex": 1,
        "yAxisIndex": 1,
        "itemStyle" : {
          "color": 'lightblue'
        },
        "large" : True,
        "encode": {
          "x": 0,
          "y": 5
        }
      },
    ]
  }

  return options

# histogram distribution
def _dataframe_to_histogramchart_options(data: pd.Series, bins: int = 10, title: str = None):
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

def _parse_data_for_json(x):
  if isinstance(x, pd.Timestamp) or isinstance(x, pd.Timedelta):
    return str(x)
  return x

def _statistics_to_json(stats: pd.Series, pnl: pd.Series):
  result = {}
  for i in range(len(stats.index)):
    key = stats.index[i]
    if not key.startswith("_"):
      result[key] = _parse_data_for_json(stats.values[i])
  
  profits = pnl[pnl > 0]
  losses = pnl[pnl < 0]
  profit_min = profits.min()
  profit_max = profits.max()
  profit_avg = profits.sum() / len(profits)
  loss_min = losses.max() # I use max function because losses are negative values, same reasoning for losses_max
  loss_max = losses.min()
  loss_avg = losses.sum() / len(losses)
  profits_less_then_10_count = len(profits[profits < 10])

  result["Min. Profit"] = profit_min
  result["Max. Profit"] = profit_max
  result["Avg. Profit"] = profit_avg

  result["Min. Loss"] = loss_min
  result["Max. Loss"] = loss_max
  result["Avg. Loss"] = loss_avg

  result["Profit less then 10 USD count"] = profits_less_then_10_count

  return result

def _trades_to_json(data: pd.DataFrame):
  result = {}

  for key in data.columns:
    df = data[key].map(_parse_data_for_json)
    result[key] = df.values.tolist()

  return result

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
        "color": viridis_cmap_hex_colors
      }
    },
    "series": series
  }
  return options

def _parse_heatmap_series(heatmap: pd.Series):
  if not isinstance(heatmap, pd.Series) or heatmap.empty:
    return []
  
  params_combinations = combinations(heatmap.index.names, 2)
  dataframes = [heatmap.groupby(list(dimensions)).agg("mean").to_frame(name="_Value") for dimensions in params_combinations]

  options = [_dataframe_to_heatmapchart_options(df) for df in dataframes]
  return options

METHODS_SOURCE_CODE = """
  function plot_echart(container, option) {
    if (container == null || option == null) return;
    const chart = echarts.init(container);
    chart.setOption(option);
    return chart;
  }

  function plot_stats(container, stats) {
    if (container == null || stats == null || Object.keys(stats).length == 0) return;
    const rows = [];
    for (const stat_name in stats) {
      const value = stats[stat_name];
      const formatted_value = typeof value == "number" ? value.toFixed(2) : value;
      rows.push(`<tr><td>${stat_name}</td><td>${formatted_value}</td></tr>`);
    }
    container.innerHTML = `<table><tbody>${rows.join('')}</tbody></table>`;
  }

  function plot_table(container, data) {
    if (container == null || data == null || Object.keys(data).length == 0) return null;

    const columns    = Object.keys(data);//.filter(key => key != "index");
    const table_head = `<thead><tr>${columns.map(key => `<th>${key}</th>`).join('')}</tr></thead>`;
    const size = data[columns[0]].length;
    const rows = [];
    for (let i = 0; i < size; i++) {
      const values = [];
      for (const column_name of columns) {
        values.push(`<td>${data[column_name][i]}</td>`);
      }
      rows.push(`<tr>${values.join('')}</tr>`);
    }

    const table_body    = `<tbody>${rows.join('')}</tbody>`;

    container.innerHTML = `<table>${table_head}${table_body}</table>`;
  }
  
  function plot_heatmaps(container, options) {
    if (container == null || options == null) return;
    if (!options.length) return;

    options.forEach(option => {
      const chart_container = document.createElement("div");
      chart_container.classList.add("heatmap");
      container.appendChild(chart_container);
      plot_echart(chart_container, option);
    });
  }
"""

STYLE_CODE = """
  html, body {
    padding: 0;
    margin : 0;
  }

  .page-title {
    text-align: center;
  }

  main {
    display    : flex;
    flex-flow  : column;
    align-items: center;
    gap        : 40px;
  }

  .statistics {
    width: 100%;
  }

  .statistics > h3 {
    text-align: center;
  }

  .statistics > .columns {
    display        : flex;
    justify-content: center;
    width          : 100%;
  }

  .metrics__row {
    display        : flex;
    justify-content: center;
  }

  .metric {
    width : 500px;
    height: 300px;
  }

  .metric--big {
    width : 1500px;
    height: 500px;
  }

  .heatmap {
    width: 1500px;
    height: 500px;
  }

  #candlestick-chart {
    width : 1500px;
    height: 800px;
  }

  #histogram {
    width : 1500px;
    height: 500px;
  }

  #equity {
    width : 1500px;
    height: 500px;
  }

  #trades {
    margin-bottom: 40px;
  }

  #trades table {
    display       : block;
    overflow      : auto;
    height        : 400px;
    border-spacing: 0;
  }

  #trades th,
  #trades td {
    padding: 4px 8px;
  }

  #trades thead th {
    position        : sticky;
    top             : 0;
    vertical-align  : bottom;
    background-color: #fff;
  }

  #trades tbody {
    white-space: nowrap;
  }

  #trades tbody tr:nth-child(even) {
    background-color: #ccc;
  }

  #loader {
    position        : fixed;
    left            : 0;
    top             : 0;
    right           : 0;
    bottom          : 0;
    background-color: #141414;
    color           : #eee;
    display         : flex;
    justify-content : center;
    align-items     : center;
    overflow        : auto;
  }

  #loader > p {
    text-align: center;
    font-size : 42px;
  }

  .report-performances ul {
    list-style: none;
    font-size : 22px;
  }
"""

# https://echarts.apache.org/examples/en/editor.html?c=heatmap-cartesian
def report_html(context: Context, parent_folder: str, file_suffix: str = "", strategy_name: str = None):
  """
  Save the result statistics and metrics as html page report.

  `context` Context of the pipeline, see `strategy_tester.pipeline.context.Context`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  `strategy_name` (optional) Name of the backtested strategy
  """
  stats = context.stats
  heatmap = context.heatmap
  equity_curve = stats["_equity_curve"]
  trades = stats["_trades"]
  ohlcv = context.data

  profits_losses_sum_by_hour = context.metrics["profits_losses_sum_by_hour"]
  profits_losses_sum_by_dow = context.metrics["profits_losses_sum_by_dow"]
  profits_losses_sum_by_month = context.metrics["profits_losses_sum_by_month"]

  profits_losses_by_hour = context.metrics["profits_losses_by_hour"]
  profits_losses_by_dow = context.metrics["profits_losses_by_dow"]
  profits_losses_by_month = context.metrics["profits_losses_by_month"]

  entries_by_hour = context.metrics["entries_by_hour"]
  entries_by_dow = context.metrics["entries_by_dow"]
  entries_by_month = context.metrics["entries_by_month"]

  # profits_losses_mean_by_hour = context.metrics["profits_losses_mean_by_hour"]
  # profits_losses_mean_by_dow = context.metrics["profits_losses_mean_by_dow"]
  # profits_losses_mean_by_month = context.metrics["profits_losses_mean_by_month"]

  profits_by_time_opened = context.metrics["profits_by_time_opened"]
  losses_by_time_opened = context.metrics["losses_by_time_opened"]

  statistics_json = _statistics_to_json(stats, trades["PnL"])

  equity_chart_options = _dataseries_to_linechart_options(equity_curve["Equity"], "Equity")

  profits_losses_sum_by_hour_chart_options = _dataseries_to_stacked_barchart_options_splitted_by_zeroline(profits_losses_sum_by_hour, "Profits sum by Hour")
  profits_losses_sum_by_dow_chart_options = _dataseries_to_stacked_barchart_options_splitted_by_zeroline(profits_losses_sum_by_dow, "Profits sum by Day of week")
  profits_losses_sum_by_month_chart_options = _dataseries_to_stacked_barchart_options_splitted_by_zeroline(profits_losses_sum_by_month, "Profits sum by Month")

  profits_losses_by_hour_chart_options = _dataframe_to_grouped_barchart_options(profits_losses_by_hour, "Profits/Losses by Hour")
  profits_losses_by_dow_chart_options = _dataframe_to_grouped_barchart_options(profits_losses_by_dow, "Profits/Losses by Day of week")
  profits_losses_by_month_chart_options = _dataframe_to_grouped_barchart_options(profits_losses_by_month, "Profits/Losses by Month")

  entries_by_hour_chart_options = _dataframe_to_grouped_barchart_options(entries_by_hour, "Entries by Hour")
  entries_by_dow_chart_options = _dataframe_to_grouped_barchart_options(entries_by_dow, "Entries by Day of week")
  entries_by_month_chart_options = _dataframe_to_grouped_barchart_options(entries_by_month, "Entries by Month")

  profits_by_time_opened_chart_options = _dataframe_to_scatterchart_cartesian_options(profits_by_time_opened, ["BarsCount", "PnL"], "Profits by time")
  losses_by_time_opened_chart_options = _dataframe_to_scatterchart_cartesian_options(losses_by_time_opened, ["BarsCount", "PnL"], "Losses by time")

  pnl_distribution = _dataframe_to_histogramchart_options(trades["PnL"], 100, "PnL distribution")

  candlestick_chart_options = _dataframe_to_candlestickchart_options(ohlcv, trades)

  trades_json = _trades_to_json(trades)

  heatmaps_chart_options = _parse_heatmap_series(heatmap)

  data_source = {
    "strategy_name": strategy_name,
    "statistics": statistics_json,
    "equity_chart_options": equity_chart_options,
    "metrics": {
      "profits_losses_sum_by_hour": profits_losses_sum_by_hour_chart_options,
      "profits_losses_sum_by_dow": profits_losses_sum_by_dow_chart_options,
      "profits_losses_sum_by_month": profits_losses_sum_by_month_chart_options,
      "profits_losses_by_hour": profits_losses_by_hour_chart_options,
      "profits_losses_by_dow": profits_losses_by_dow_chart_options,
      "profits_losses_by_month": profits_losses_by_month_chart_options,
      "entries_by_hour": entries_by_hour_chart_options,
      "entries_by_dow": entries_by_dow_chart_options,
      "entries_by_month": entries_by_month_chart_options,
      "profits_by_time_opened": profits_by_time_opened_chart_options,
      "losses_by_time_opened": losses_by_time_opened_chart_options,
      "pnl_distribution": pnl_distribution,
    },
    "candlestick": candlestick_chart_options,
    "trades": trades_json,
    "heatmaps": heatmaps_chart_options,
  }

  data_source_json = json.dumps(data_source, ensure_ascii=False)
  data_source_code = f"window.data_source = {data_source_json};"
  data_source_code_base64 = str(base64.b64encode(data_source_code.encode())).split("'")[1]
  
  methods_source_code_base64 = str(base64.b64encode(METHODS_SOURCE_CODE.encode())).split("'")[1]

  html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0"><title>BTCUSD - Stochastic RSI reversal strategy</title>
      <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"></script>
      <script type="text/javascript" src="data:text/javascript;base64,{data_source_code_base64}"></script>
      <script type="text/javascript" src="data:text/javascript;base64,{methods_source_code_base64}"></script>
      <style>
        {STYLE_CODE}
      </style>
    </head>
    <body>
      <header>
        <h1 class="page-title">{strategy_name if strategy_name else "Strategy report"}</h1>
      </header>

      <main>

        <div class="statistics">
          <h3>Statistics</h3>
          <div class="columns">
            <div id="stats"></div>
            <div id="extra-stats"></div>
          </div>
        </div>

        <div class="equity-curve">
          <div id="equity"></div>
        </div>

        <div class="metrics">
          <div class="metrics__row">
            <div id="profits_losses_sum_by_hour" class="metric"></div>
            <div id="profits_losses_sum_by_dow" class="metric"></div>
            <div id="profits_losses_sum_by_month" class="metric"></div>
          </div>
          <div class="metrics__row">
            <div id="profits_losses_by_hour" class="metric"></div>
            <div id="profits_losses_by_dow" class="metric"></div>
            <div id="profits_losses_by_month" class="metric"></div>
          </div>
          <div class="metrics__row">
            <div id="entries_count_by_hour" class="metric"></div>
            <div id="entries_count_by_dow" class="metric"></div>
            <div id="entries_count_by_month" class="metric"></div>
          </div>
          <div class="metrics__row">
            <div id="profits_by_time_opened" class="metric metric--big"></div>
          </div>
          <div class="metrics__row">
            <div id="losses_by_time_opened" class="metric metric--big"></div>
          </div>
          <div class="metrics__row">
            <div id="pnl_distribution" class="metric metric--big"></div>
          </div>
        </div>

        <div id="heatmaps-container"></div>

        <div id="candlestick-chart"></div>

        <div id="trades"></div>
      </main>

      <script>
        plot_stats(document.getElementById("stats"), data_source["statistics"]);
        
        plot_echart(document.getElementById("equity"), data_source["equity_chart_options"]);

        plot_echart(document.getElementById("profits_losses_sum_by_hour"), data_source["metrics"]["profits_losses_sum_by_hour"]);
        plot_echart(document.getElementById("profits_losses_sum_by_dow"), data_source["metrics"]["profits_losses_sum_by_dow"]);
        plot_echart(document.getElementById("profits_losses_sum_by_month"), data_source["metrics"]["profits_losses_sum_by_month"]);
        
        plot_echart(document.getElementById("profits_losses_by_hour"), data_source["metrics"]["profits_losses_by_hour"]);
        plot_echart(document.getElementById("profits_losses_by_dow"), data_source["metrics"]["profits_losses_by_dow"]);
        plot_echart(document.getElementById("profits_losses_by_month"), data_source["metrics"]["profits_losses_by_month"]);
        
        plot_echart(document.getElementById("entries_count_by_hour"), data_source["metrics"]["entries_by_hour"]);
        plot_echart(document.getElementById("entries_count_by_dow"), data_source["metrics"]["entries_by_dow"]);
        plot_echart(document.getElementById("entries_count_by_month"), data_source["metrics"]["entries_by_month"]);

        plot_echart(document.getElementById("profits_by_time_opened"), data_source["metrics"]["profits_by_time_opened"]);
        plot_echart(document.getElementById("losses_by_time_opened"), data_source["metrics"]["losses_by_time_opened"]);
        
        plot_echart(document.getElementById("pnl_distribution"), data_source["metrics"]["pnl_distribution"]);

        plot_heatmaps(document.getElementById("heatmaps-container"), data_source["heatmaps"]);

        plot_echart(document.getElementById("candlestick-chart"), data_source["candlestick"])
        
        plot_table(document.getElementById("trades"), data_source["trades"]);
      </script>
    </body>
  """

  file_suffix = '_' + file_suffix if file_suffix != "" else ""
  with open(f"{parent_folder}/report{file_suffix}.html", "w", encoding="utf-8") as file:
    file.write(html)