# from datetime import datetime
import pandas as pd
from ..utils.files import _create_file_suffix

def save_metrics(entries_bars_by_hour: pd.DataFrame, entries_bars_by_dow: pd.DataFrame, entries_bars_by_month: pd.DataFrame,
                profits_losses_by_hour: pd.DataFrame, profits_losses_by_dow: pd.DataFrame, profits_losses_by_month: pd.DataFrame,
                profits_losses_mean_by_hour: pd.Series, profits_losses_mean_by_dow: pd.Series, profits_losses_mean_by_month: pd.Series,
                profits_losses_sum_by_hour: pd.Series, profits_losses_sum_by_dow: pd.Series, profits_losses_sum_by_month: pd.Series,
                profits_by_time_opened: pd.DataFrame, losses_by_time_opened: pd.DataFrame,
                parent_folder:str, file_suffix = ""):
  """
  Save metrics as separated csv.

  `entris_bars_by_hour` entries by hour metric.\n
  `entris_bars_by_dow` entries by day of week metric.\n
  `entris_bars_by_month` entries by month metric.\n

  `profits_losses_by_hour` profits/losses by hour metric.\n
  `profits_losses_by_dow` profits/losses by day of week metric.\n
  `profits_losses_by_month` profits/losses by month metric.\n

  `profits_losses_mean_by_hour` mean of profits and losses by hour metric.\n
  `profits_losses_mean_by_dow` mean of profits and losses by day of week metric.\n
  `profits_losses_mean_by_month` mean of profits and losses by month metric.\n

  `profits_losses_sum_by_hour` sum of profits and losses by hour metric.\n
  `profits_losses_sum_by_dow` sum of profits and losses by day of week metric.\n
  `profits_losses_sum_by_month` sum of profits and losses by month metric.\n

  `profits_by_time_opened` profits by bar count metric.\n
  `losses_by_time_opened` losses by bar count metric.\n

  `parent_folder` folder where to save the csv.\n
  
  `file_suffix` optional file suffix to customize the file name.\n
  """
  file_suffix = _create_file_suffix(file_suffix)

  if not entries_bars_by_hour.empty:
    entries_bars_by_hour_filename = f"{parent_folder}/entries_by_hour{file_suffix}.csv"
    entries_bars_by_hour.to_csv(entries_bars_by_hour_filename)
  
  if not entries_bars_by_dow.empty:
    entries_bars_by_dow_filename = f"{parent_folder}/entries_by_dow{file_suffix}.csv"
    entries_bars_by_dow.to_csv(entries_bars_by_dow_filename)
  
  if not entries_bars_by_month.empty:
    entries_bars_by_month_filename = f"{parent_folder}/entries_by_month{file_suffix}.csv"
    entries_bars_by_month.to_csv(entries_bars_by_month_filename)

  if not profits_losses_by_hour.empty:
    profits_losses_by_hour_filename = f"{parent_folder}/profits_losses_by_hour{file_suffix}.csv"
    profits_losses_by_hour.to_csv(profits_losses_by_hour_filename)

  if not profits_losses_by_dow.empty:
    profits_losses_by_dow_filename = f"{parent_folder}/profits_losses_by_dow{file_suffix}.csv"
    profits_losses_by_dow.to_csv(profits_losses_by_dow_filename)
  
  if not profits_losses_by_month.empty:
    profits_losses_by_month_filename = f"{parent_folder}/profits_losses_by_month{file_suffix}.csv"
    profits_losses_by_month.to_csv(profits_losses_by_month_filename)

  if not profits_losses_mean_by_hour.empty:
    profits_losses_mean_by_hour_filename = f"{parent_folder}/profits_losses_mean_by_hour{file_suffix}.csv"
    pd.DataFrame(profits_losses_mean_by_hour).to_csv(profits_losses_mean_by_hour_filename)

  if not profits_losses_mean_by_dow.empty:
    profits_losses_mean_by_dow_filename = f"{parent_folder}/profits_losses_mean_by_dow{file_suffix}.csv"
    pd.DataFrame(profits_losses_mean_by_dow).to_csv(profits_losses_mean_by_dow_filename)
  
  if not profits_losses_mean_by_month.empty:
    profits_losses_mean_by_month_filename = f"{parent_folder}/profits_losses_mean_by_month{file_suffix}.csv"
    pd.DataFrame(profits_losses_mean_by_month).to_csv(profits_losses_mean_by_month_filename)

  if not profits_losses_sum_by_hour.empty:
    profits_losses_sum_by_hour_filename = f"{parent_folder}/profits_losses_sum_by_hour{file_suffix}.csv"
    pd.DataFrame(profits_losses_sum_by_hour).to_csv(profits_losses_sum_by_hour_filename)
  
  if not profits_losses_sum_by_dow.empty:
    profits_losses_sum_by_dow_filename = f"{parent_folder}/profits_losses_sum_by_dow{file_suffix}.csv"
    pd.DataFrame(profits_losses_sum_by_dow).to_csv(profits_losses_sum_by_dow_filename)
  
  if not profits_losses_sum_by_month.empty:
    profits_losses_sum_by_month_filename = f"{parent_folder}/profits_losses_sum_by_month{file_suffix}.csv"
    pd.DataFrame(profits_losses_sum_by_month).to_csv(profits_losses_sum_by_month_filename)

  if not profits_by_time_opened.empty:
    profits_by_time_opened_filename = f"{parent_folder}/profits_by_time_opened{file_suffix}.csv"
    profits_by_time_opened.to_csv(profits_by_time_opened_filename)
  
  if not losses_by_time_opened.empty:
    losses_by_time_opened_filename = f"{parent_folder}/losses_by_time_opened{file_suffix}.csv"
    losses_by_time_opened.to_csv(losses_by_time_opened_filename)