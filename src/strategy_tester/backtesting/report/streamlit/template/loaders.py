import json

import pandas as pd
import streamlit as st


@st.cache_data
def load_statistics():
  with open("./data/stats.json", "r") as file:
    parsed = json.loads(file.read())
    return parsed

@st.cache_data
def load_broker_params():
  with open("./data/broker_params.txt", "r") as file:
    return "\n".join(file.readlines())

@st.cache_data
def load_strategy_params():
  with open("./data/strategy_params.txt", "r") as file:
    return "\n".join(file.readlines())

@st.cache_data
def load_equity_curve():
  equity_curve = pd.read_csv("./data/equity.csv")
  equity_curve["Date"] = pd.to_datetime(equity_curve["Date"])
  equity_curve.set_index("Date", inplace=True)
  return equity_curve

@st.cache_data
def load_profits_losses_sum_by_hour():
  return pd.read_csv("./data/profits_losses_sum_by_hour.csv")

@st.cache_data
def load_profits_losses_sum_by_dow():
  return pd.read_csv("./data/profits_losses_sum_by_dow.csv")

@st.cache_data
def load_profits_losses_sum_by_month():
  return pd.read_csv("./data/profits_losses_sum_by_month.csv")

@st.cache_data
def load_profits_losses_mean_by_hour():
  return pd.read_csv("./data/profits_losses_mean_by_hour.csv")

@st.cache_data
def load_profits_losses_mean_by_dow():
  return pd.read_csv("./data/profits_losses_mean_by_dow.csv")

@st.cache_data
def load_profits_losses_mean_by_month():
  return pd.read_csv("./data/profits_losses_mean_by_month.csv")

@st.cache_data
def load_profits_losses_by_hour():
  return pd.read_csv("./data/profits_losses_by_hour.csv")

@st.cache_data
def load_profits_losses_by_dow():
  return pd.read_csv("./data/profits_losses_by_dow.csv")

@st.cache_data
def load_profits_losses_by_month():
  return pd.read_csv("./data/profits_losses_by_month.csv")

@st.cache_data
def load_entries_by_hour():
  return pd.read_csv("./data/entries_by_hour.csv")

@st.cache_data
def load_entries_by_dow():
  return pd.read_csv("./data/entries_by_dow.csv")

@st.cache_data
def load_entries_by_month():
  return pd.read_csv("./data/entries_by_month.csv")

@st.cache_data
def load_profits_by_time_opened():
  return pd.read_csv("./data/profits_by_time_opened.csv")

@st.cache_data
def load_losses_by_time_opened():
  return pd.read_csv("./data/losses_by_time_opened.csv")

@st.cache_data
def load_trades():
  return pd.read_csv("./data/trades.csv")

@st.cache_data
def load_ohlcv():
  ohlcv = pd.read_csv("./data/ohlcv.csv")
  ohlcv["Date"] = pd.to_datetime(ohlcv["Date"])
  return ohlcv
