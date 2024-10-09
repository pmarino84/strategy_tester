"""
Module with helper functions to calculate some useful metric from the backtest/optimization results.

The metrics that you can calculate are:\n
+ entries by hour, see `.entries_counts.get_entries_by_hour`\n
+ entries by day of week, see `.entries_counts.get_entries_by_dayofweek`\n
+ entries by month, see `.entries_counts.get_entries_by_month`\n
+ profits losses by hour, see `.profits_losses_bars.get_profits_losses_by_hour`\n
+ profits losses by day of week, see `.profits_losses_bars.get_profits_losses_by_dayofweek`\n
+ profits losses by month, see `.profits_losses_bars.get_profits_losses_by_month`\n
+ profits by time opened, see `.profits_losses_by_bar_opened.get_profits_by_time_opened`\n
+ losses by time opened, see `.profits_losses_by_bar_opened.get_losses_by_time_opened`\n
+ profits/losses mean by hour, see `.profits_losses_mean.get_profits_losses_mean_by_hour`\n
+ profits/losses mean by day of week, see `.profits_losses_mean.get_profits_losses_mean_by_dayofweek`\n
+ profits/losses mean by month, see `.profits_losses_mean.get_profits_losses_mean_by_month`\n
+ profits/losses sum by hour, see `.profits_losses_sum.get_profits_losses_sum_by_hour`\n
+ profits/losses sum by day of week, see `.profits_losses_sum.get_profits_losses_sum_bydayofweek`\n
+ profits/losses sum by month, see `.profits_losses_sum.get_profits_losses_sum_by_month`\n\n

Others helper functions are:\n
+ `plot_metrics` to plot statistics and metrics with the matplot lib, see `.report_pdf.plot_metrics`\n
+ `report_to_pdf` to save statistics and metrics as pdf, see `.report_pdf.report_to_pdf`\n
+ `save_metrics` to save metrics data as csv, see `.save.save_metrics`\n
"""

from .entries_counts import get_entries_by_hour, get_entries_by_dayofweek, get_entries_by_month
from .profits_losses_bars import get_profits_losses_by_hour, get_profits_losses_by_dayofweek, get_profits_losses_by_month
from .profits_losses_by_bar_opened import get_profits_by_time_opened, get_losses_by_time_opened
from .profits_losses_mean import get_profits_losses_mean_by_hour, get_profits_losses_mean_by_dayofweek, get_profits_losses_mean_by_month
from .profits_losses_sum import get_profits_losses_sum_by_hour, get_profits_losses_sum_by_dayofweek, get_profits_losses_sum_by_month
from ..report.pdf.report_pdf import plot_metrics, report_to_pdf
from .save import save_metrics
