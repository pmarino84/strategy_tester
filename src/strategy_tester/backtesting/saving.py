import pandas as pd

from ..pipeline.context import Context
from ..storage.save_dataframe import save_dataframe_as_csv


def save_equity(stats: pd.Series, parent_folder: str) -> None:
  """
  Save the equity curve as csv

  `stats` statistics `pd.Series` where to find the equity curve\n
  `parent_folder` folder where to save the file\n
  """
  save_dataframe_as_csv(stats["_equity_curve"], parent_folder, "equity_curve.csv", reset_index=True, index_name="Date")

def save_statistics_to_json(stats: pd.Series, parent_folder: str) -> None:
  """
  Save the statistics as json

  `stats` statistics `pd.Series`\n
  `parent_folder` folder where to save the file\n
  """
  stats_file_name = f"{parent_folder}/stats.json"
  stats_filtered = pd.DataFrame(stats).copy().T
  stats_filtered.drop(columns=["_strategy", "_equity_curve", "_trades"], inplace=True)
  stats_filtered = stats_filtered.T
  stats_filtered[0].to_json(stats_file_name)

def save_statistics_to_csv(stats: pd.Series, parent_folder: str) -> None:
  """
  Save the statistics as csv

  `stats` statistics `pd.Series`\n
  `parent_folder` folder where to save the file\n
  """
  stats_columns = [x for x in stats.index if x not in ["_strategy", "_equity_curve", "_trades"]]
  save_dataframe_as_csv(pd.DataFrame(stats).T, parent_folder, "stats.csv", columns=stats_columns)

def save_trades(context: Context, folder: str = "") -> None:
  """
  Save the trades as csv

  `stats` statistics `pd.Series` where to find the trades\n
  """
  result_folder = context.result_folder
  if folder != "":
    result_folder += f"/{folder}"
  save_dataframe_as_csv(context.custom["trades"], result_folder, "trades.csv")

def save_ohlcv_data(ohlcv: pd.DataFrame, parent_folder: str) -> None:
  """
  Save the OHLCV data as csv

  `ohlcv` data to save `pd.DataFrame`\n
  `parent_folder` folder where to save the file\n
  """
  file_name = f"{parent_folder}/ohlcv.csv"
  ohlcv.reset_index(inplace=True)
  ohlcv.rename(columns={ "index": "Date" }, inplace=True)
  ohlcv.to_csv(file_name, index=False)

def save_backtest_results(context: Context, folder: str = "") -> None:
  """
  Save the statistics, equity curve and trades on files.

  `context` Pipeline context\n
  """
  result_folder = context.result_folder
  if folder != "":
    result_folder += f"/{folder}"
  save_equity(context.stats, result_folder)
  save_statistics_to_json(context.stats, result_folder)
  save_statistics_to_csv(context.stats, result_folder)
  save_trades(context)

def save_heatmap(heatmap: pd.DataFrame, parent_folder: str) -> None:
  """
  Save the heatmap as csv

  `stats` heatmap `pd.DataFrame`\n
  `parent_folder` folder where to save the file\n
  """
  file_name = f"{parent_folder}/heatmap.csv"
  heatmap.to_csv(file_name)

def save_optimization_results(context: Context) -> None:
  """
  Save the statistics, heatmap, equity curve and trades on files.

  `stats` statistics `pd.Series` with equity curve and trades also\n
  `heatmap` optimized params heatmap `pd.Series`\n
  `parent_folder` folder where to save the file\n
  """
  save_backtest_results(context)
  save_heatmap(context.heatmap, context.result_folder)