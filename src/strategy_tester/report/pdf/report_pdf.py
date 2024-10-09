import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from ...pipeline.context import Context
from ._add_equity import _add_equity
from ._add_heatmap import _add_heatmap
from ._add_metadata import _add_metadata
from ._add_metrics import _add_metrics
from ._add_statistics import _add_statistics


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

# TODO: aggiungere profits_losses_mean_by_hour/dow/month
def report_to_pdf(context: Context, pdf_title = "", author = "", subject = "", keyworkds = ""):
  """
  Save statistics and metrics as pdf.

  `context` pipeline result context.\n
  
  `pdf_title` (optional) pdf title metadata.\n
  `author` (optional) pdf Author metadata.\n
  `subject` (optional) pdf Subject metadata.\n
  `keywords` (optional) pdf Keywords metadata.\n
  """
  statistics = context.stats

  if statistics.empty:
    # if there isn't statistics data also there isn't metrics, equity, heatmap...
    return

  file_path = f"{context.result_folder}/report.pdf"
  with PdfPages(file_path) as pdf:
    _add_statistics(pdf, statistics)

    _add_equity(pdf, statistics["_equity_curve"]["Equity"])

    _add_metrics(pdf, context.metrics)

    _add_heatmap(pdf, context.heatmap)

    _add_metadata(pdf, pdf_title, author, subject, keyworkds)
