from typing import Dict, Union

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _add_metrics(pdf: PdfPages, metrics: Dict[str, Union[pd.DataFrame, pd.Series]]):
  profits_losses_sum_by_hour = metrics["profits_losses_sum_by_hour"] if "profits_losses_sum_by_hour" in metrics else pd.DataFrame()
  profits_losses_sum_by_dow = metrics["profits_losses_sum_by_dow"] if "profits_losses_sum_by_dow" in metrics else pd.DataFrame()
  profits_losses_sum_by_month = metrics["profits_losses_sum_by_month"] if "profits_losses_sum_by_month" in metrics else pd.DataFrame()

  profits_losses_by_hour = metrics["profits_losses_by_hour"] if "profits_losses_by_hour" in metrics else pd.DataFrame()
  profits_losses_by_dow = metrics["profits_losses_by_dow"] if "profits_losses_by_dow" in metrics else pd.DataFrame()
  profits_losses_by_month = metrics["profits_losses_by_month"] if "profits_losses_by_month" in metrics else pd.DataFrame()

  entries_by_hour = metrics["entries_by_hour"] if "entries_by_hour" in metrics else pd.DataFrame()
  entries_by_dow = metrics["entries_by_dow"] if "entries_by_dow" in metrics else pd.DataFrame()
  entries_by_month = metrics["entries_by_month"] if "entries_by_month" in metrics else pd.DataFrame()

  # profits_losses_mean_by_hour = metrics["profits_losses_mean_by_hour"] if "profits_losses_mean_by_hour" in metrics else pd.DataFrame()
  # profits_losses_mean_by_dow = metrics["profits_losses_mean_by_dow"] if "profits_losses_mean_by_dow" in metrics else pd.DataFrame()
  # profits_losses_mean_by_month = metrics["profits_losses_mean_by_month"] if "profits_losses_mean_by_month" in metrics else pd.DataFrame()

  profits_by_time_opened = metrics["profits_by_time_opened"] if "profits_by_time_opened" in metrics else pd.DataFrame()
  losses_by_time_opened = metrics["losses_by_time_opened"] if "losses_by_time_opened" in metrics else pd.DataFrame()

  if not profits_losses_sum_by_hour.empty and not profits_losses_sum_by_dow.empty and not profits_losses_sum_by_month.empty:
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

  if not profits_losses_by_hour.empty and not profits_losses_by_dow.empty and not profits_losses_by_month.empty:
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

  if not entries_by_hour.empty and not entries_by_dow.empty and not entries_by_month.empty:
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

  if not profits_by_time_opened.empty:
    plt.figure(figsize=(16, 8))
    profits_by_time_opened.plot.scatter(x="BarsCount", y="PnL", c="blue", figsize=(16,8))
    plt.title("Profits vs time opened")
    pdf.savefig()
    plt.close()
    
  if not losses_by_time_opened.empty:
    plt.figure(figsize=(16, 8))
    losses_by_time_opened.plot.scatter(x="BarsCount", y="PnL", c="red", figsize=(16,8))
    plt.title("Losses vs time opened")
    pdf.savefig()
    plt.close()