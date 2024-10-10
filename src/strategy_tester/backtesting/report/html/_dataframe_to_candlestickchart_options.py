import pandas as pd


def _dataframe_to_candlestickchart_options(ohlcv: pd.DataFrame, trades: pd.DataFrame):
  if ohlcv.empty or trades.empty:
    return None
  
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
