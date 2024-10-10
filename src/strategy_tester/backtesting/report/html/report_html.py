import base64
import json

import pandas as pd

from ....pipeline.context import Context
from ._dataframe_to_candlestickchart_options import _dataframe_to_candlestickchart_options
from ._dataframe_to_grouped_barchart_options import _dataframe_to_grouped_barchart_options
from ._dataframe_to_histogramchart_options import _dataframe_to_histogramchart_options
from ._dataframe_to_scatterchart_cartesian_options import _dataframe_to_scatterchart_cartesian_options
from ._dataseries_to_linechart_options import _dataseries_to_linechart_options
from ._dataseries_to_stacked_barchart_options_splitted_by_zeroline import _dataseries_to_stacked_barchart_options_splitted_by_zeroline
from ._heatmap import _parse_heatmap_series
from ._statistics_to_json import _statistics_to_json
from ._trades_to_json import _trades_to_json

_METHODS_SOURCE_CODE = """
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

_MAIN_SCRIPT = """
  plot_stats(document.getElementById("stats"), data_source["statistics"]);

  if (data_source["equity_chart_options"]) {
    document.getElementById("equity").classList.remove("hide");
    plot_echart(document.getElementById("equity"), data_source["equity_chart_options"]);
  }

  if (data_source["metrics"]["profits_losses_sum_by_hour"]) {
    document.getElementById("profits_losses_sum_by_hour").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_sum_by_hour"), data_source["metrics"]["profits_losses_sum_by_hour"]);
  }

  if (data_source["metrics"]["profits_losses_sum_by_dow"]) {
    document.getElementById("profits_losses_sum_by_dow").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_sum_by_dow"), data_source["metrics"]["profits_losses_sum_by_dow"]);
  }

  if (data_source["metrics"]["profits_losses_sum_by_month"]) {
    document.getElementById("profits_losses_sum_by_month").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_sum_by_month"), data_source["metrics"]["profits_losses_sum_by_month"]);
  }
  
  if (data_source["metrics"]["profits_losses_by_hour"]) {
    document.getElementById("profits_losses_by_hour").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_by_hour"), data_source["metrics"]["profits_losses_by_hour"]);
  }
  
  if (data_source["metrics"]["profits_losses_by_dow"]) {
    document.getElementById("profits_losses_by_dow").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_by_dow"), data_source["metrics"]["profits_losses_by_dow"]);
  }
  
  if (data_source["metrics"]["profits_losses_by_month"]) {
    document.getElementById("profits_losses_by_month").classList.remove("hide");
    plot_echart(document.getElementById("profits_losses_by_month"), data_source["metrics"]["profits_losses_by_month"]);
  }
  
  if (data_source["metrics"]["entries_by_hour"]) {
    document.getElementById("entries_count_by_hour").classList.remove("hide");
    plot_echart(document.getElementById("entries_count_by_hour"), data_source["metrics"]["entries_by_hour"]);
  }
  
  if (data_source["metrics"]["entries_by_dow"]) {
    document.getElementById("entries_count_by_dow").classList.remove("hide");
    plot_echart(document.getElementById("entries_count_by_dow"), data_source["metrics"]["entries_by_dow"]);
  }
  
  if (data_source["metrics"]["entries_by_month"]) {
    document.getElementById("entries_count_by_month").classList.remove("hide");
    plot_echart(document.getElementById("entries_count_by_month"), data_source["metrics"]["entries_by_month"]);
  }

  if (data_source["metrics"]["profits_by_time_opened"]) {
    document.getElementById("profits_by_time_opened").classList.remove("hide");
    plot_echart(document.getElementById("profits_by_time_opened"), data_source["metrics"]["profits_by_time_opened"]);
  }
  
  if (data_source["metrics"]["losses_by_time_opened"]) {
    document.getElementById("losses_by_time_opened").classList.remove("hide");
    plot_echart(document.getElementById("losses_by_time_opened"), data_source["metrics"]["losses_by_time_opened"]);
  }
  
  if (data_source["metrics"]["pnl_distribution"]) {
    document.getElementById("pnl_distribution").classList.remove("hide");
    plot_echart(document.getElementById("pnl_distribution"), data_source["metrics"]["pnl_distribution"]);
  }

  plot_heatmaps(document.getElementById("heatmaps-container"), data_source["heatmaps"]);

  if (data_source["candlestick"]) {
    document.getElementById("candlestick-chart").classList.remove("hide");
    plot_echart(document.getElementById("candlestick-chart"), data_source["candlestick"]);
  }
  
  if (data_source["trades"]) {
    document.getElementById("trades").classList.remove("hide");
    plot_table(document.getElementById("trades"), data_source["trades"]);
  }
"""

_STYLE_CODE = """
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

  .hide {
    display: none;
  }
"""

# TODO: aggiungere profits_losses_mean_by_hour/dow/month
def report_to_html(context: Context, file_suffix: str = ""):
  """
  Save the result statistics and metrics as html page report.

  `context` Context of the pipeline, see `strategy_tester.pipeline.context.Context`\n
  `file_suffix` file name suffix to customize it's name\n
  """
  stats = context.stats

  if stats.empty:
    # if there isn't statistics data also there isn't metrics, equity, heatmap...
    return

  heatmap = context.heatmap
  equity_curve = stats["_equity_curve"]
  trades = stats["_trades"]
  ohlcv = context.data

  metrics = context.metrics
  profits_losses_sum_by_hour = metrics["profits_losses_sum_by_hour"] if "profits_losses_sum_by_hour" in metrics else pd.DataFrame()
  profits_losses_sum_by_dow = metrics["profits_losses_sum_by_dow"] if "profits_losses_sum_by_dow" in metrics else pd.DataFrame()
  profits_losses_sum_by_month = metrics["profits_losses_sum_by_month"] if "profits_losses_sum_by_month" in metrics else pd.DataFrame()

  profits_losses_by_hour = metrics["profits_losses_by_hour"] if "profits_losses_by_hour" in metrics else pd.DataFrame()
  profits_losses_by_dow = metrics["profits_losses_by_dow"] if "profits_losses_by_dow" in metrics else pd.DataFrame()
  profits_losses_by_month = metrics["profits_losses_by_month"] if "profits_losses_by_month" in metrics else pd.DataFrame()

  entries_by_hour = metrics["entries_by_hour"] if "entries_by_hour" in metrics else pd.DataFrame()
  entries_by_dow = metrics["entries_by_dow"] if "entries_by_dow" in metrics else pd.DataFrame()
  entries_by_month = metrics["entries_by_month"] if "entries_by_month" in metrics else pd.DataFrame()

  # profits_losses_mean_by_hour = metrics["profits_losses_mean_by_hour"] if "profits_losses_mean_by_hour" in metrics else pd.DataFrame()
  # profits_losses_mean_by_dow = metrics["profits_losses_mean_by_dow"] if "profits_losses_mean_by_dow" in metrics else pd.DataFrame()
  # profits_losses_mean_by_month = metrics["profits_losses_mean_by_month"] if "profits_losses_mean_by_month" in metrics else pd.DataFrame()

  profits_by_time_opened = metrics["profits_by_time_opened"] if "profits_by_time_opened" in metrics else pd.DataFrame()
  losses_by_time_opened = metrics["losses_by_time_opened"] if "losses_by_time_opened" in metrics else pd.DataFrame()

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

  strategy_name = context.strategy_name or context.strategy.__name__
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
  
  methods_source_code_base64 = str(base64.b64encode(_METHODS_SOURCE_CODE.encode())).split("'")[1]

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
        {_STYLE_CODE}
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
          <div id="equity" class="hide"></div>
        </div>

        <div class="metrics">
          <div class="metrics__row">
            <div id="profits_losses_sum_by_hour" class="metric hide"></div>
            <div id="profits_losses_sum_by_dow" class="metric hide"></div>
            <div id="profits_losses_sum_by_month" class="metric hide"></div>
          </div>
          <div class="metrics__row">
            <div id="profits_losses_by_hour" class="metric hide"></div>
            <div id="profits_losses_by_dow" class="metric hide"></div>
            <div id="profits_losses_by_month" class="metric hide"></div>
          </div>
          <div class="metrics__row">
            <div id="entries_count_by_hour" class="metric hide"></div>
            <div id="entries_count_by_dow" class="metric hide"></div>
            <div id="entries_count_by_month" class="metric hide"></div>
          </div>
          <div class="metrics__row">
            <div id="profits_by_time_opened" class="metric metric--big hide"></div>
          </div>
          <div class="metrics__row">
            <div id="losses_by_time_opened" class="metric metric--big hide"></div>
          </div>
          <div class="metrics__row">
            <div id="pnl_distribution" class="metric metric--big hide"></div>
          </div>
        </div>

        <div id="heatmaps-container"></div>

        <div id="candlestick-chart" class="hide"></div>

        <div id="trades" class="hide"></div>
      </main>

      <script>
        {_MAIN_SCRIPT}
      </script>
    </body>
  """

  file_suffix = '_' + file_suffix if file_suffix != "" else ""
  with open(f"{context.result_folder}/report{file_suffix}.html", "w", encoding="utf-8") as file:
    file.write(html)