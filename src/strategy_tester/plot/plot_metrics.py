import matplotlib.pyplot as plt
import pandas as pd

from ..pipeline.context import Context


def plot_metrics(context: Context):
  """
  Plot statistics, equity and metrics with the help of `matplotlib`.

  `context` backtest/optimization pipeline result context.\n
  """
  stats = context.stats

  if stats.empty:
    # nothing to draw
    return

  fig, axes = plt.subplot_mosaic("JJJ;KKK;ABC;DEF;GHI;LLL;MMM", figsize=(16,20))

  axes["J"].axis("off")
  table = pd.plotting.table(ax=axes["J"], data=stats, bbox=[0.5, -0.3, 0.3, 2.6])
  table.set_fontsize(10)
  table_dict = table.get_celld()
  table_dict[0, 0].set_text_props(text="Statistics")

  stats["_equity_curve"]["Equity"].plot.line(ax=axes["K"])
  axes["K"].set_title("Equity")

  metrics = context.metrics
  profits_losses_sum_by_hour = metrics["profits_losses_sum_by_hour"] if "profits_losses_sum_by_hour" in metrics else pd.DataFrame()
  profits_losses_sum_by_dow = metrics["profits_losses_sum_by_dow"] if "profits_losses_sum_by_dow" in metrics else pd.DataFrame()
  profits_losses_sum_by_month = metrics["profits_losses_sum_by_month"] if "profits_losses_sum_by_month" in metrics else pd.DataFrame()

  profits_losses_mean_by_hour = metrics["profits_losses_mean_by_hour"] if "profits_losses_mean_by_hour" in metrics else pd.DataFrame()
  profits_losses_mean_by_dow = metrics["profits_losses_mean_by_dow"] if "profits_losses_mean_by_dow" in metrics else pd.DataFrame()
  profits_losses_mean_by_month = metrics["profits_losses_mean_by_month"] if "profits_losses_mean_by_month" in metrics else pd.DataFrame()

  profits_losses_by_hour = metrics["profits_losses_by_hour"] if "profits_losses_by_hour" in metrics else pd.DataFrame()
  profits_losses_by_dow = metrics["profits_losses_by_dow"] if "profits_losses_by_dow" in metrics else pd.DataFrame()
  profits_losses_by_month = metrics["profits_losses_by_month"] if "profits_losses_by_month" in metrics else pd.DataFrame()

  entries_by_hour = metrics["entries_by_hour"] if "entries_by_hour" in metrics else pd.DataFrame()
  entries_by_dow = metrics["entries_by_dow"] if "entries_by_dow" in metrics else pd.DataFrame()
  entries_by_month = metrics["entries_by_month"] if "entries_by_month" in metrics else pd.DataFrame()

  profits_by_time_opened = metrics["profits_by_time_opened"] if "profits_by_time_opened" in metrics else pd.DataFrame()
  losses_by_time_opened = metrics["losses_by_time_opened"] if "losses_by_time_opened" in metrics else pd.DataFrame()

  entries_color = { "entries_profits": "green", "entries_losses": "red" }

  if not entries_by_hour.empty:
    entries_by_hour.plot.bar(ax=axes["A"], color=entries_color)
    axes["A"].set_title("Entries by Hour")
    axes["A"].legend().remove()
    axes["A"].set_xlabel("")
  
  if not entries_by_dow.empty:
    entries_by_dow.plot.bar(ax=axes["B"], color=entries_color)
    axes["B"].set_title("Entries by Day Of Week")
    axes["B"].legend().remove()
    axes["B"].set_xlabel("")
    
  if not entries_by_month.empty:
    entries_by_month.plot.bar(ax=axes["C"], color=entries_color)
    axes["C"].set_title("Entries by Month")
    axes["C"].legend().remove()
    axes["C"].set_xlabel("")

  profits_losses_color = { "profits": "green", "losses": "red" }

  if not profits_losses_by_hour.empty:
    profits_losses_by_hour.plot.bar(ax=axes["D"], color=profits_losses_color)
    axes["D"].set_title("Profits/Losses by Hour")
    axes["D"].legend().remove()
    axes["D"].set_xlabel("")

  if not profits_losses_by_dow.empty:
    profits_losses_by_dow.plot.bar(ax=axes["E"], color=profits_losses_color)
    axes["E"].set_title("Profits/Losses by Day Of Week")
    axes["E"].legend().remove()
    axes["E"].set_xlabel("")

  if not profits_losses_by_month.empty:
    profits_losses_by_month.plot.bar(ax=axes["F"], color=profits_losses_color)
    axes["F"].set_title("Profits/Losses by Month")
    axes["F"].legend().remove()
    axes["F"].set_xlabel("")

  if not profits_losses_sum_by_hour.empty:
    profits_losses_sum_by_hour_colors = profits_losses_sum_by_hour.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_hour.plot.bar(ax=axes["G"], color=profits_losses_sum_by_hour_colors)
    axes["G"].set_title("Profits/Losses Sum by Hour")
    axes["G"].legend().remove()
    axes["G"].set_xlabel("")

  if not profits_losses_sum_by_dow.empty:
    profits_losses_sum_by_dow_colors = profits_losses_sum_by_dow.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_dow.plot.bar(ax=axes["H"], color=profits_losses_sum_by_dow_colors)
    axes["H"].set_title("Profits/Losses Sum by Day Of Week")
    axes["H"].legend().remove()
    axes["H"].set_xlabel("")

  if not profits_losses_sum_by_month.empty:
    profits_losses_sum_by_month_colors = profits_losses_sum_by_month.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_sum_by_month.plot.bar(ax=axes["I"], color=profits_losses_sum_by_month_colors)
    axes["I"].set_title("Profits/Losses Sum by Month")
    axes["I"].legend().remove()
    axes["I"].set_xlabel("")

  if not profits_losses_mean_by_hour.empty:
    profits_losses_mean_by_hour_colors = profits_losses_mean_by_hour.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_mean_by_hour.plot.bar(ax=axes["G"], color=profits_losses_mean_by_hour_colors)
    axes["G"].set_title("Profits/Losses Mean by Hour")
    axes["G"].legend().remove()
    axes["G"].set_xlabel("")

  if not profits_losses_mean_by_dow.empty:
    profits_losses_mean_by_dow_colors = profits_losses_mean_by_dow.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_mean_by_dow.plot.bar(ax=axes["H"], color=profits_losses_mean_by_dow_colors)
    axes["H"].set_title("Profits/Losses Mean by Day Of Week")
    axes["H"].legend().remove()
    axes["H"].set_xlabel("")

  if not profits_losses_mean_by_month.empty:
    profits_losses_mean_by_month_colors = profits_losses_mean_by_month.map(lambda x: "green" if x > 0 else "red").to_list()
    profits_losses_mean_by_month.plot.bar(ax=axes["I"], color=profits_losses_mean_by_month_colors)
    axes["I"].set_title("Profits/Losses Mean by Month")
    axes["I"].legend().remove()
    axes["I"].set_xlabel("")

  if not profits_by_time_opened.empty:
    profits_by_time_opened.plot.scatter(ax=axes["L"], x="BarsCount", y="PnL", c="blue")
  
  if not losses_by_time_opened.empty:
    losses_by_time_opened.plot.scatter(ax=axes["M"], x="BarsCount", y="PnL", c="red")

  fig.subplots_adjust(hspace=0.5)
  plt.show()
