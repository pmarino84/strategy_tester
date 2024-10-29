from datetime import date, timedelta

import plotly.graph_objs as go
import streamlit as st
from loaders import *
from matplotlib import pyplot as plt

st.set_page_config(page_title="GOOG Backtest", layout="wide")

st.title("GOOG Backtest")

st.markdown("""<style>
  [data-testid="stHeadingDivider"] {
    background-color: #FF4B4B;
  }
</style>""", unsafe_allow_html=True)

PROFITS_COLOR   = "#23c7dc"
LOSSES_COLOR    = "#e52791"

stats           = load_statistics()
broker_params   = load_broker_params()
strategy_params = load_strategy_params()
trades          = load_trades()
ohlcv           = load_ohlcv()

statistics_tab, params_tab = st.tabs(["Statistics", "Parameters"])

initial_balance = 0
for row in broker_params.split("\n"):
  if "cash" in row:
    initial_balance = float(row.split("=")[1])

equity_final          = stats["Equity Final [$]"]
equity_peak           = stats["Equity Peak [$]"]
equity_delta          = round(equity_final / initial_balance * 100, 2)
sharpe_ratio          = stats["Sharpe Ratio"]
sortino_ratio         = stats["Sortino Ratio"]
calmar_ratio          = stats["Calmar Ratio"]
profit_factor         = stats["Profit Factor"]
expectancy            = stats["Expectancy [%]"]
sqn                   = stats["SQN"]
return_pct            = stats["Return [%]"]
buy_and_hold_ret_pct  = stats["Buy & Hold Return [%]"]
return_ann_pct        = stats["Return (Ann.) [%]"]
volatility_ann_pct    = stats["Volatility (Ann.) [%]"]
win_rate_pct          = stats["Win Rate [%]"]
best_trade_pct        = stats["Best Trade [%]"]
worst_trade_pct       = stats["Worst Trade [%]"]
avg_trade_pct         = stats["Avg. Trade [%]"]
max_drawdown_pct      = stats["Max. Drawdown [%]"]
avg_drawdown_pct      = stats["Avg. Drawdown [%]"]
max_drawdown_duration = stats["Max. Drawdown Duration"]
avg_drawdown_duration = stats["Avg. Drawdown Duration"]
trades_count          = stats["# Trades"]
max_trade_duration    = stats["Max. Trade Duration"]
avg_trade_duration    = stats["Avg. Trade Duration"]
start_time            = stats["Start"]
end_time              = stats["End"]
duration              = stats["Duration"]
exposure              = stats["Exposure Time [%]"]

with statistics_tab:
  cell_11, cell_12, cell_13, cell_14 = st.columns(4)
  cell_21, cell_22, cell_23, cell_24 = st.columns(4)

  with cell_11:
    with st.container(border=True, height=200):
      st.metric("Equity", value=f"{round(equity_final, 2)}$", delta=f"{equity_delta}%")
      st.text(f"Initial: {round(initial_balance, 2)}$ (Peak: {round(equity_peak, 2)}$)")
  
  with cell_12:
    with st.container(border=True, height=200):
      st.text(F"Sharpe Ratio: {round(sharpe_ratio, 2)}")
      st.text(F"Sortino Ratio: {round(sortino_ratio, 2)}")
      st.text(F"Calmar Ratio: {round(calmar_ratio, 2)}")
  
  with cell_13:
    with st.container(border=True, height=200):
      st.text(F"Profit Factor: {round(profit_factor, 2)}")
      st.text(F"Expectancy: {round(expectancy, 2)}%")
      st.text(F"SQN: {round(sqn, 2)}")
  
  with cell_14:
    with st.container(border=True, height=200):
      st.text(f"Return: {round(return_pct, 2)}%")
      st.text(f"Buy and hold return: {round(buy_and_hold_ret_pct, 2)}%")
      st.text(f"Return (Ann.): {round(return_ann_pct, 2)}%")
      st.text(f"Volatility (Ann.): {round(volatility_ann_pct, 2)}%")
  
  with cell_21:
    with st.container(border=True, height=200):
      st.text(f"Win rate: {round(win_rate_pct)}%")
      st.text(f"Best trade: {round(best_trade_pct)}%")
      st.text(f"Worst trade: {round(worst_trade_pct)}%")
      st.text(f"Avg. trade: {round(avg_trade_pct)}%")

  with cell_22:
    with st.container(border=True, height=200):
      st.text(f"Max. drawdown: {round(max_drawdown_pct, 2)}%")
      st.text(f"Avg. drawdown: {round(avg_drawdown_pct, 2)}%")
      st.text(f"Max. drawdown duration: {timedelta(seconds=max_drawdown_duration / 1000)}")
      st.text(f"Avg. drawdown duration: {timedelta(seconds=avg_drawdown_duration / 1000)}")

  with cell_23:
    with st.container(border=True, height=200):
      st.text(f"# Trades: {trades_count}")
      st.text(f"Max. trade duration: {timedelta(seconds=max_trade_duration / 1000)}")
      st.text(f"Avg. trade duration: {timedelta(seconds=avg_trade_duration / 1000)}")
  
  with cell_24:
    with st.container(border=True, height=200):
      st.text(f"Start: {date.fromtimestamp(start_time / 1000)}")
      st.text(f"End: {date.fromtimestamp(end_time / 1000)}")
      st.text(f"Duration: {timedelta(seconds=duration / 1000)}")
      st.text(f"Exposure Time: {round(exposure, 2)}%")

with params_tab:
  strategy_params_col, broker_params_col = st.columns(2)
  
  with strategy_params_col:
    with st.container(border=True):
      st.write(strategy_params)
  
  with broker_params_col:
    with st.container(border=True):
      st.write(broker_params)

st.header("Equity", divider=True)
equity_curve = load_equity_curve()
st.line_chart(equity_curve["Equity"])

st.header("Metrics", divider=True)
col1, col2, col3 = st.columns(3)
with col1:
  st.header("Profit losses sum by hour")
  profits_losses_sum_by_hour = load_profits_losses_sum_by_hour().copy()
  profits_losses_sum_by_hour["color"] = profits_losses_sum_by_hour["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_sum_by_hour, x="hour", y="PnL", color="color")

with col2:
  st.header("Profit losses sum by dow")
  profits_losses_sum_by_dow = load_profits_losses_sum_by_dow().copy()
  profits_losses_sum_by_dow["color"] = profits_losses_sum_by_dow["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_sum_by_dow, x="day_of_week", y="PnL", color="color")

with col3:
  st.header("Profit losses sum by month")
  profits_losses_sum_by_month = load_profits_losses_sum_by_month().copy()
  profits_losses_sum_by_month["color"] = profits_losses_sum_by_month["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_sum_by_month, x="month", y="PnL", color="color")

col4, col5, col6 = st.columns(3)

with col4:
  st.header("Profit losses mean by hour")
  profits_losses_mean_by_hour = load_profits_losses_mean_by_hour().copy()
  profits_losses_mean_by_hour["color"] = profits_losses_mean_by_hour["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_mean_by_hour, x="hour", y="PnL", color="color")

with col5:
  st.header("Profit losses mean by dow")
  profits_losses_mean_by_dow = load_profits_losses_mean_by_dow().copy()
  profits_losses_mean_by_dow["color"] = profits_losses_mean_by_dow["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_mean_by_dow, x="day_of_week", y="PnL", color="color")

with col6:
  st.header("Profit losses mean by month")
  profits_losses_mean_by_month = load_profits_losses_mean_by_month().copy()
  profits_losses_mean_by_month["color"] = profits_losses_mean_by_month["PnL"].map(lambda x: PROFITS_COLOR if x >= 0 else LOSSES_COLOR)
  st.bar_chart(profits_losses_mean_by_month, x="month", y="PnL", color="color")

col7, col8, col9 = st.columns(3)

with col7:
  st.header("Profits/losses by hour")
  st.bar_chart(load_profits_losses_by_hour(), x="hour", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

with col8:
  st.header("Profits/losses by dow")
  st.bar_chart(load_profits_losses_by_dow(), x="day_of_week", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

with col9:
  st.header("Profits/losses by month")
  st.bar_chart(load_profits_losses_by_month(), x="month", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

col10, col11, col12 = st.columns(3)

with col10:
  st.header("Entries by hour")
  st.bar_chart(load_entries_by_hour(), x="hour", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

with col11:
  st.header("Entries by dow")
  st.bar_chart(load_entries_by_dow(), x="day_of_week", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

with col12:
  st.header("Entries by month")
  st.bar_chart(load_entries_by_month(), x="month", stack=False, color=[PROFITS_COLOR, LOSSES_COLOR])

st.header("Profits vs bar count")
st.scatter_chart(load_profits_by_time_opened(), x="BarsCount", y="PnL", color=PROFITS_COLOR)

st.header("Losses vs bar count")
st.scatter_chart(load_losses_by_time_opened(), x="BarsCount", y="PnL", color=LOSSES_COLOR)

# TODO: si perde l'immagine
# st.header("PnL Distribution")
# pnl = trades["PnL"]
# fig, axis = plt.subplots(figsize=(16, 8))
# axis.hist(pnl, bins=100)
# st.pyplot(fig)

st.header("Trades", divider=True)
selected_trades_event = st.dataframe(trades, use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
selected_trades = [trades.iloc[i] for i in selected_trades_event.selection.rows]

st.header("Candlestick chart")
if len(selected_trades) == 0:
  st.text("Select a trade to see the candlestick chart")
bar_offset = st.number_input("Bar offset", min_value=3, max_value=30, value=10, disabled=len(selected_trades) == 0)
for selected_trade in selected_trades:
  # st.text("Selected trade:")
  # st.dataframe(selected_trade, use_container_width=True)
  first_bar_index = selected_trade["EntryBar"] - bar_offset
  last_bar_index = selected_trade["ExitBar"] + bar_offset
  if first_bar_index < 0:
    first_bar_index = 0
  if last_bar_index >= ohlcv.size:
    last_bar_index = ohlcv.size - 1
  entry_bar = ohlcv.iloc[selected_trade["EntryBar"]]
  exit_bar = ohlcv.iloc[selected_trade["ExitBar"]]
  # st.text("Entry bar:")
  # st.dataframe(entry_bar, use_container_width=True)
  # st.text("Exit bar:")
  # st.dataframe(exit_bar, use_container_width=True)
  bars = ohlcv.iloc[first_bar_index:last_bar_index]
  # st.text("Bars:")
  # st.dataframe(bars, use_container_width=True)

  candlestick = go.Candlestick(x=bars["Date"], open=bars["Open"], high=bars["High"], low=bars["Low"], close=bars["Close"])
  signals     = go.Scatter(x=[entry_bar["Date"], exit_bar["Date"]], y=[selected_trade["EntryPrice"], selected_trade["ExitPrice"]], mode="markers", marker=dict(color="violet", size=8), name="Signals")
  line        = go.Scatter(x=[entry_bar["Date"], exit_bar["Date"]], y=[selected_trade["EntryPrice"], selected_trade["ExitPrice"]], mode="lines", line=dict(color='violet', width=2), name="Trade")
  # fig = go.Figure(data=[candlestick])
  fig = go.Figure(data=[candlestick, line])
  # fig = go.Figure(data=[candlestick, signals])
  # fig = go.Figure(data=[candlestick, signals, line])

  fig.update_layout(xaxis_rangeslider_visible=False, height=600)
  st.plotly_chart(fig)

st.header("OHLCV", divider=True)
st.dataframe(ohlcv, use_container_width=True)