# from datetime import datetime
import pandas as pd
from ..utils.files import _create_file_suffix

def save_metrics(entries_bars_by_hour: pd.DataFrame, entries_bars_by_dow: pd.DataFrame, entries_bars_by_month: pd.DataFrame,
                profits_losses_by_hour: pd.DataFrame, profits_losses_by_dow: pd.DataFrame, profits_losses_by_month: pd.DataFrame,
                profits_losses_mean_by_hour: pd.Series, profits_losses_mean_by_dow: pd.Series, profits_losses_mean_by_month: pd.Series,
                profits_losses_sum_by_hour: pd.Series, profits_losses_sum_by_dow: pd.Series, profits_losses_sum_by_month: pd.Series,
                profits_by_time_opened: pd.DataFrame, losses_by_time_opened: pd.DataFrame,
                parent_folder:str, file_suffix = ""):
  file_suffix = _create_file_suffix(file_suffix)
  entries_bars_by_hour_filename = f"{parent_folder}/entries_by_hour{file_suffix}.csv"
  entries_bars_by_dow_filename = f"{parent_folder}/entries_by_dow{file_suffix}.csv"
  entries_bars_by_month_filename = f"{parent_folder}/entries_by_month{file_suffix}.csv"
  entries_bars_by_hour.to_csv(entries_bars_by_hour_filename)
  entries_bars_by_dow.to_csv(entries_bars_by_dow_filename)
  entries_bars_by_month.to_csv(entries_bars_by_month_filename)

  profits_losses_by_hour_filename = f"{parent_folder}/profits_losses_by_hour{file_suffix}.csv"
  profits_losses_by_dow_filename = f"{parent_folder}/profits_losses_by_dow{file_suffix}.csv"
  profits_losses_by_month_filename = f"{parent_folder}/profits_losses_by_month{file_suffix}.csv"
  profits_losses_by_hour.to_csv(profits_losses_by_hour_filename)
  profits_losses_by_dow.to_csv(profits_losses_by_dow_filename)
  profits_losses_by_month.to_csv(profits_losses_by_month_filename)

  profits_losses_mean_by_hour_filename = f"{parent_folder}/profits_losses_mean_by_hour{file_suffix}.csv"
  profits_losses_mean_by_dow_filename = f"{parent_folder}/profits_losses_mean_by_dow{file_suffix}.csv"
  profits_losses_mean_by_month_filename = f"{parent_folder}/profits_losses_mean_by_month{file_suffix}.csv"
  pd.DataFrame(profits_losses_mean_by_hour).to_csv(profits_losses_mean_by_hour_filename)
  pd.DataFrame(profits_losses_mean_by_dow).to_csv(profits_losses_mean_by_dow_filename)
  pd.DataFrame(profits_losses_mean_by_month).to_csv(profits_losses_mean_by_month_filename)

  profits_losses_sum_by_hour_filename = f"{parent_folder}/profits_losses_sum_by_hour{file_suffix}.csv"
  profits_losses_sum_by_dow_filename = f"{parent_folder}/profits_losses_sum_by_dow{file_suffix}.csv"
  profits_losses_sum_by_month_filename = f"{parent_folder}/profits_losses_sum_by_month{file_suffix}.csv"
  pd.DataFrame(profits_losses_sum_by_hour).to_csv(profits_losses_sum_by_hour_filename)
  pd.DataFrame(profits_losses_sum_by_dow).to_csv(profits_losses_sum_by_dow_filename)
  pd.DataFrame(profits_losses_sum_by_month).to_csv(profits_losses_sum_by_month_filename)

  profits_by_time_opened_filename = f"{parent_folder}/profits_by_time_opened{file_suffix}.csv"
  losses_by_time_opened_filename = f"{parent_folder}/losses_by_time_opened{file_suffix}.csv"
  profits_by_time_opened.to_csv(profits_by_time_opened_filename)
  losses_by_time_opened.to_csv(losses_by_time_opened_filename)