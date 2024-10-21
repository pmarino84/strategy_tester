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
+ `save_metrics` to save metrics data as csv, see `.save.save_metrics`\n
"""
