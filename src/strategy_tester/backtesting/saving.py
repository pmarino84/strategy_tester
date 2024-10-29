import pandas as pd

from ..pipeline.context import Context
from ..utils.files import create_file_suffix


def save_equity(stats: pd.Series, parent_folder: str, file_suffix = "") -> None:
  """
  Save the equity curve as csv

  `stats` statistics `pd.Series` where to find the equity curve\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  equity_file_name = f"{parent_folder}/equity{file_suffix}.csv"
  equity_curve = stats["_equity_curve"].copy()
  equity_curve.reset_index(inplace=True)
  equity_curve.rename(columns={ "index": "Date" }, inplace=True)
  equity_curve.to_csv(equity_file_name, index=False)

def save_statistics_to_json(stats: pd.Series, parent_folder: str, file_suffix = "") -> None:
  """
  Save the statistics as json

  `stats` statistics `pd.Series`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  stats_file_name = f"{parent_folder}/stats{file_suffix}.json"
  stats_filtered = pd.DataFrame(stats).copy().T
  stats_filtered.drop(columns=["_strategy", "_equity_curve", "_trades"], inplace=True)
  stats_filtered = stats_filtered.T
  stats_filtered[0].to_json(stats_file_name)

def save_statistics_to_csv(stats: pd.Series, parent_folder: str, file_suffix = "") -> None:
  """
  Save the statistics as csv

  `stats` statistics `pd.Series`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  stats_file_name = f"{parent_folder}/stats{file_suffix}.csv"
  stats_filtered = pd.DataFrame(stats).copy().T
  stats_filtered.drop(columns=["_strategy", "_equity_curve", "_trades"], inplace=True)
  stats_filtered.to_csv(stats_file_name, index=False)

def save_trades(context: Context, folder: str = "", file_suffix = "") -> None:
  """
  Save the trades as csv

  `stats` statistics `pd.Series` where to find the trades\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  result_folder = context.result_folder
  if folder != "":
    result_folder += f"/{folder}"
  trades_file_name = f"{result_folder}/trades{file_suffix}.csv"
  trades = context.custom["trades_copy"]
  trades.to_csv(trades_file_name, index=False)

def save_ohlcv_data(ohlcv: pd.DataFrame, parent_folder: str, file_suffix: str = "") -> None:
  """
  Save the OHLCV data as csv

  `ohlcv` data to save `pd.DataFrame`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  file_name = f"{parent_folder}/ohlcv{file_suffix}.csv"
  ohlcv.reset_index(inplace=True)
  ohlcv.rename(columns={ "index": "Date" }, inplace=True)
  ohlcv.to_csv(file_name, index=False)

def save_backtest_results(context: Context, folder: str = "", file_suffix: str = "") -> None:
  """
  Save the statistics, equity curve and trades on files.

  `context` Pipeline context\n
  `file_suffix` file name suffix to customize it's name\n
  """
  result_folder = context.result_folder
  if folder != "":
    result_folder += f"/{folder}"
  save_equity(context.stats, result_folder, file_suffix)
  save_statistics_to_json(context.stats, result_folder, file_suffix)
  save_statistics_to_csv(context.stats, result_folder, file_suffix)
  save_trades(context, file_suffix)

def save_heatmap(heatmap: pd.DataFrame, parent_folder: str, file_suffix = "") -> None:
  """
  Save the heatmap as csv

  `stats` heatmap `pd.DataFrame`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  file_suffix = create_file_suffix(file_suffix)
  file_name = f"{parent_folder}/heatmap{file_suffix}.csv"
  heatmap.to_csv(file_name)

# def save_optimization_results(stats: pd.Series, heatmap: pd.DataFrame, parent_folder: str, file_suffix = "") -> None:
def save_optimization_results(context: Context, file_suffix = "") -> None:
  """
  Save the statistics, heatmap, equity curve and trades on files.

  `stats` statistics `pd.Series` with equity curve and trades also\n
  `heatmap` optimized params heatmap `pd.Series`\n
  `parent_folder` folder where to save the file\n
  `file_suffix` file name suffix to customize it's name\n
  """
  save_backtest_results(context, file_suffix)
  save_heatmap(context.heatmap, context.result_folder, file_suffix)