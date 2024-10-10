from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages


# reference: https://stackoverflow.com/questions/12286607/making-heatmap-from-pandas-dataframe
def _conv_index_to_bins(index):
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

def _calc_df_mesh(df: pd.DataFrame):
    """Calculate the two-dimensional bins to hold the index and column values."""
    return np.meshgrid(_conv_index_to_bins(df.index.copy()), _conv_index_to_bins(df.columns))

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
      X, Y = _calc_df_mesh(df)

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
      X, Y = _calc_df_mesh(df)
      c = plt.pcolormesh(X, Y, df.values.T)
      plt.colorbar(c, ax=axes[i])
      axes[i].set_title(f"{first_name} x {second_name}")
      axes[i].set_xlabel(first_name)
      axes[i].set_ylabel(second_name)
      _add_cell_values_to_heatmap(df, axes[i])

      fig.subplots_adjust(hspace=0.8)
      pdf.savefig(fig)
    plt.close()
