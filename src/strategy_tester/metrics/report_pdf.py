from datetime import datetime
from itertools import combinations
from typing import Dict, Union

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


# TODO: spostare in appropriato file, non centra nulla con report pdf
# TODO: aggiungere profits_losses_mean_by_hour/dow/month
def plot_metrics(entris_bars_by_hour: pd.DataFrame, entris_bars_by_dow: pd.DataFrame, entris_bars_by_month: pd.DataFrame,
                profits_losses_by_hour: pd.DataFrame, profits_losses_by_dow: pd.DataFrame, profits_losses_by_month: pd.DataFrame,
                profits_losses_sum_by_hour: pd.Series, profits_losses_sum_by_dow: pd.Series, profits_losses_sum_by_month: pd.Series,
                profits_by_time_opened: pd.DataFrame, losses_by_time_opened: pd.DataFrame,
                equity: pd.Series, statistics: pd.Series):
  """
  Plot statistics and metrics with the help of `matplotlib`.

  `entris_bars_by_hour` entries by hour metric.\n
  `entris_bars_by_dow` entries by day of week metric.\n
  `entris_bars_by_month` entries by month metric.\n

  `profits_losses_by_hour` profits/losses by hour metric.\n
  `profits_losses_by_dow` profits/losses by day of week metric.\n
  `profits_losses_by_month` profits/losses by month metric.\n

  `profits_losses_sum_by_hour` sum of profits and losses by hour metric.\n
  `profits_losses_sum_by_dow` sum of profits and losses by day of week metric.\n
  `profits_losses_sum_by_month` sum of profits and losses by month metric.\n

  `profits_by_time_opened` profits by bar count metric.\n
  `losses_by_time_opened` losses by bar count metric.\n
  """
  fig, axes = plt.subplot_mosaic("JJJ;KKK;ABC;DEF;GHI;LLL;MMM", figsize=(16,20))

  axes["J"].axis("off")
  table = pd.plotting.table(ax=axes["J"], data=statistics, bbox=[0.5, -0.3, 0.3, 2.6])
  table.set_fontsize(10)
  table_dict = table.get_celld()
  table_dict[0, 0].set_text_props(text="Statistics")

  equity.plot.line(ax=axes["K"])
  axes["K"].set_title("Equity")

  entries_color = { "entries_profits": "green", "entries_losses": "red" }
  entris_bars_by_hour.plot.bar(ax=axes["A"], color=entries_color)
  axes["A"].set_title("Entries by Hour")
  axes["A"].legend().remove()
  axes["A"].set_xlabel("")
  
  entris_bars_by_dow.plot.bar(ax=axes["B"], color=entries_color)
  axes["B"].set_title("Entries by Day Of Week")
  axes["B"].legend().remove()
  axes["B"].set_xlabel("")
  
  entris_bars_by_month.plot.bar(ax=axes["C"], color=entries_color)
  axes["C"].set_title("Entries by Month")
  axes["C"].legend().remove()
  axes["C"].set_xlabel("")

  profits_losses_color = { "profits": "green", "losses": "red" }
  profits_losses_by_hour.plot.bar(ax=axes["D"], color=profits_losses_color)
  axes["D"].set_title("Profits/Losses by Hour")
  axes["D"].legend().remove()
  axes["D"].set_xlabel("")

  profits_losses_by_dow.plot.bar(ax=axes["E"], color=profits_losses_color)
  axes["E"].set_title("Profits/Losses by Day Of Week")
  axes["E"].legend().remove()
  axes["E"].set_xlabel("")

  profits_losses_by_month.plot.bar(ax=axes["F"], color=profits_losses_color)
  axes["F"].set_title("Profits/Losses by Month")
  axes["F"].legend().remove()
  axes["F"].set_xlabel("")

  profits_losses_sum_by_hour_colors = profits_losses_sum_by_hour.map(lambda x: "green" if x > 0 else "red").to_list()
  profits_losses_sum_by_hour.plot.bar(ax=axes["G"], color=profits_losses_sum_by_hour_colors)
  axes["G"].set_title("Profits/Losses Sum by Hour")
  axes["G"].legend().remove()
  axes["G"].set_xlabel("")

  profits_losses_sum_by_dow_colors = profits_losses_sum_by_dow.map(lambda x: "green" if x > 0 else "red").to_list()
  profits_losses_sum_by_dow.plot.bar(ax=axes["H"], color=profits_losses_sum_by_dow_colors)
  axes["H"].set_title("Profits/Losses Sum by Day Of Week")
  axes["H"].legend().remove()
  axes["H"].set_xlabel("")

  profits_losses_sum_by_month_colors = profits_losses_sum_by_month.map(lambda x: "green" if x > 0 else "red").to_list()
  profits_losses_sum_by_month.plot.bar(ax=axes["I"], color=profits_losses_sum_by_month_colors)
  axes["I"].set_title("Profits/Losses Sum by Month")
  axes["I"].legend().remove()
  axes["I"].set_xlabel("")

  profits_by_time_opened.plot.scatter(ax=axes["L"], x="BarsCount", y="PnL", c="blue")
  losses_by_time_opened.plot.scatter(ax=axes["M"], x="BarsCount", y="PnL", c="red")

  fig.subplots_adjust(hspace=0.5)
  plt.show()


def _add_cell_values_to_heatmap(df: pd.DataFrame, ax: Axes):
  for i, row in df.iterrows():
      for j, value in row.items():
        formatted_value = round(value, 2)
        ax.text(i, j, formatted_value, horizontalalignment="center", verticalalignment="center", color="white")

def _add_heatmap(pdf: PdfPages, heatmap: pd.Series):
  if isinstance(heatmap, pd.Series) and not heatmap.empty:
    # print(heatmap)
    # print(heatmap.unstack())
    params_combinations = combinations(heatmap.index.names, 2)
    dataframes = [heatmap.groupby(list(dimensions)).agg("mean").to_frame(name="_Value") for dimensions in params_combinations]

    if len(dataframes) == 1:
      df = dataframes[0]
      # print(df)
      first_name, second_name = df.index.names
      df = df.unstack()
      df.columns = df.columns.droplevel()
      # print(df)
      X, Y = calc_df_mesh(df)

      plt.figure(figsize=(16, 8))
      c = plt.pcolormesh(X, Y, df.values.T)
      plt.colorbar(c)
      # plt.gca().set_title(f"{first_name} x {second_name}")
      plt.title(f"{first_name} x {second_name}")
      plt.gca().set_xlabel(first_name)
      plt.gca().set_ylabel(second_name)

      _add_cell_values_to_heatmap(df, plt.gca())

      pdf.savefig()
      plt.close()
      return

    fig, axes = plt.subplots(len(dataframes), 1, figsize=(16, 14))
    for i in range(len(dataframes)):
      # print(f"Histogram {i}")
      df = dataframes[i]

      first_name, second_name = df.index.names
      # first_levels = df.index.levels[0].to_list()
      # first_level_min, first_level_max = min(first_levels), max(first_levels)
      # print(f"{first_name} min, max = {first_level_min}, {first_level_max}")
      # second_levels = df.index.levels[1].to_list()
      # second_level_min, second_level_max = min(second_levels), max(second_levels)
      # print(f"{second_name} min, max = {second_level_min}, {second_level_max}")
      
      df = df.unstack()
      X, Y = calc_df_mesh(df)
      c = plt.pcolormesh(X, Y, df.values.T)
      plt.colorbar(c, ax=axes[i])
      axes[i].set_title(f"{first_name} x {second_name}")
      axes[i].set_xlabel(first_name)
      axes[i].set_ylabel(second_name)
      _add_cell_values_to_heatmap(df, axes[i])

      fig.subplots_adjust(hspace=0.8)
      pdf.savefig(fig)
    plt.close()

# TODO: aggiungere profits_losses_mean_by_hour/dow/month
# TODO: spostare in altro modulo, non salva solo le metriche
def report_to_pdf(file_path: str, metrics: Dict[str, Union[pd.DataFrame, pd.Series]], statistics: pd.Series, heatmap: pd.Series = pd.Series(), pdf_title = "", author = "", subject = "", keyworkds = ""):
  """
  Save statistics and metrics as pdf.

  `file_path` saving file path.\n
  `metrics` calculated matrics dictionary.\n
  `statistics` The backtest/optimization statistics result.\n
  `heatmap` result heatmap.\n
  
  `pdf_title` (optional) pdf title metadata.\n
  `author` (optional) pdf Author metadata.\n
  `subject` (optional) pdf Subject metadata.\n
  `keywords` (optional) pdf Keywords metadata.\n
  """
  profits_losses_sum_by_hour = metrics["profits_losses_sum_by_hour"]
  profits_losses_sum_by_dow = metrics["profits_losses_sum_by_dow"]
  profits_losses_sum_by_month = metrics["profits_losses_sum_by_month"]

  profits_losses_by_hour = metrics["profits_losses_by_hour"]
  profits_losses_by_dow = metrics["profits_losses_by_dow"]
  profits_losses_by_month = metrics["profits_losses_by_month"]

  entries_by_hour = metrics["entries_by_hour"]
  entries_by_dow = metrics["entries_by_dow"]
  entries_by_month = metrics["entries_by_month"]

  # profits_losses_mean_by_hour = metrics["profits_losses_mean_by_hour"]
  # profits_losses_mean_by_dow = metrics["profits_losses_mean_by_dow"]
  # profits_losses_mean_by_month = metrics["profits_losses_mean_by_month"]

  profits_by_time_opened = metrics["profits_by_time_opened"]
  losses_by_time_opened = metrics["losses_by_time_opened"]

  equity = statistics["_equity_curve"]["Equity"]

  with PdfPages(file_path) as pdf:
    statistics_df = pd.DataFrame(statistics).copy().T
    statistics_df.drop(columns=["_strategy", "_equity_curve", "_trades"], inplace=True)
    plt.figure(figsize=(16, 16))
    plt.gca().axis("off")
    table = pd.plotting.table(ax=plt.gca(), data=statistics_df.T, bbox=[0.2, 0.1, 0.78, 0.9], colWidths=[0.7, 1])
    table.set_fontsize(12)
    table_dict = table.get_celld()
    table_dict[0, 0].set_text_props(text="Statistics")
    pdf.savefig()
    plt.close()

    plt.figure(figsize=(16, 8))
    equity.plot.line()
    plt.title("Equity")
    pdf.savefig()
    plt.close()

    fig, axes = plt.subplots(3, 1, figsize=(16, 14))
    profits_losses_sum_by_hour_colors = profits_losses_sum_by_hour.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_hour.plot.bar(ax=axes[0], color=profits_losses_sum_by_hour_colors)
    axes[0].set_title("Profits/Losses Sum by Hour")
    axes[0].legend().remove()

    profits_losses_sum_by_dow_colors = profits_losses_sum_by_dow.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_dow.plot.bar(ax=axes[1], color=profits_losses_sum_by_dow_colors)
    axes[1].set_title("Profits/Losses Sum by Day Of Week")
    axes[1].legend().remove()

    profits_losses_sum_by_month_colors = profits_losses_sum_by_month.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_month.plot.bar(ax=axes[2], color=profits_losses_sum_by_month_colors)
    axes[2].set_title("Profits/Losses Sum by Month")
    axes[2].legend().remove()

    fig.subplots_adjust(hspace=0.8)
    pdf.savefig(fig)
    plt.close()

    fig, axes = plt.subplots(3, 1, figsize=(16, 14))
    profits_losses_color = { "profits": "green", "losses": "red" }
    profits_losses_by_hour.plot.bar(ax=axes[0], color=profits_losses_color)
    axes[0].set_title("Profits/Losses by Hour")
    axes[0].legend().remove()

    profits_losses_by_dow.plot.bar(ax=axes[1], color=profits_losses_color)
    axes[1].set_title("Profits/Losses by Day Of Week")
    axes[1].legend().remove()

    profits_losses_by_month.plot.bar(ax=axes[2], color=profits_losses_color)
    axes[2].set_title("Profits/Losses by Month")
    axes[2].legend().remove()

    fig.subplots_adjust(hspace=0.8)
    pdf.savefig(fig)
    plt.close()

    fig, axes = plt.subplots(3, 1, figsize=(16, 14))
    entries_color = { "entries_profits": "green", "entries_losses": "red" }
    entries_by_hour.plot.bar(ax=axes[0], color=entries_color)
    axes[0].set_title("Entries by Hour")
    axes[0].legend().remove()
    
    entries_by_dow.plot.bar(ax=axes[1], color=entries_color)
    axes[1].set_title("Entries by Day Of Week")
    axes[1].legend().remove()
    
    entries_by_month.plot.bar(ax=axes[2], color=entries_color)
    axes[2].set_title("Entries by Month")
    axes[2].legend().remove()

    fig.subplots_adjust(hspace=0.8)
    pdf.savefig(fig)
    plt.close()

    plt.figure(figsize=(16, 8))
    profits_by_time_opened.plot.scatter(x="BarsCount", y="PnL", c="blue", figsize=(16,8))
    plt.title("Profits vs time opened")
    pdf.savefig()
    plt.close()
    
    plt.figure(figsize=(16, 8))
    losses_by_time_opened.plot.scatter(x="BarsCount", y="PnL", c="red", figsize=(16,8))
    plt.title("Losses vs time opened")
    pdf.savefig()
    plt.close()

    _add_heatmap(pdf, heatmap)

    pdf_dict = pdf.infodict()
    if pdf_title != "":
      pdf_dict["Title"] = pdf_title
    if author != "":
      pdf_dict["Author"] = author
    if subject != "":
      pdf_dict["Subject"] = subject
    if keyworkds != "":
      pdf_dict["Keywords"] = keyworkds
    pdf_dict["CreationDate"] = datetime.today()
    pdf_dict["ModificationDate"] = datetime.today()

# reference: https://stackoverflow.com/questions/12286607/making-heatmap-from-pandas-dataframe
def conv_index_to_bins(index):
    """Calculate bins to contain the index values.
    The start and end bin boundaries are linearly extrapolated from 
    the two first and last values. The middle bin boundaries are 
    midpoints.

    Example 1: [0, 1] -> [-0.5, 0.5, 1.5]
    Example 2: [0, 1, 4] -> [-0.5, 0.5, 2.5, 5.5]
    Example 3: [4, 1, 0] -> [5.5, 2.5, 0.5, -0.5]"""
    assert index.is_monotonic_increasing or index.is_monotonic_decreasing
    # print("conv_index_to_bins index:")
    # print(index)
    if isinstance(index, pd.MultiIndex):
      index = index.droplevel()
      # print(index)

    # the beginning and end values are guessed from first and last two
    start = index[0] - (index[1]-index[0])/2
    end = index[-1] + (index[-1]-index[-2])/2
    # print(f"start, end = {start}, {end}")

    # the middle values are the midpoints
    middle = pd.DataFrame({'m1': index[:-1], 'p1': index[1:]})
    middle = middle['m1'] + (middle['p1']-middle['m1'])/2
    # print("middle:")
    # print(middle)

    if isinstance(index, pd.DatetimeIndex):
        idx = pd.DatetimeIndex(middle).union([start,end])
    elif isinstance(index, (pd.Index,pd.RangeIndex)):
        idx = pd.Index(middle).union([start,end])
    else:
        # print('Warning: guessing what to do with index type %s' % 
        #       type(index))
        print(f"Warning: guessing what to do with index type {type(index)}")
        idx = pd.Index(middle).union([start,end])

    return idx.sort_values(ascending=index.is_monotonic_increasing)

def calc_df_mesh(df: pd.DataFrame):
    """Calculate the two-dimensional bins to hold the index and column values."""
    return np.meshgrid(conv_index_to_bins(df.index.copy()), conv_index_to_bins(df.columns))