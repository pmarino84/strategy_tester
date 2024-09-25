from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_metrics(entris_bars_by_hour: pd.DataFrame, entris_bars_by_dow: pd.DataFrame, entris_bars_by_month: pd.DataFrame,
                profits_losses_by_hour: pd.DataFrame, profits_losses_by_dow: pd.DataFrame, profits_losses_by_month: pd.DataFrame,
                profits_losses_sum_by_hour: pd.Series, profits_losses_sum_by_dow: pd.Series, profits_losses_sum_by_month: pd.Series,
                profits_by_time_opened: pd.DataFrame, losses_by_time_opened: pd.DataFrame,
                equity: pd.Series, statistics: pd.Series):
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

def metrics_to_pdf(entris_bars_by_hour: pd.DataFrame, entris_bars_by_dow: pd.DataFrame, entris_bars_by_month: pd.DataFrame,
              profits_losses_by_hour: pd.DataFrame, profits_losses_by_dow: pd.DataFrame, profits_losses_by_month: pd.DataFrame,
              profits_losses_sum_by_hour: pd.Series, profits_losses_sum_by_dow: pd.Series, profits_losses_sum_by_month: pd.Series,
              profits_by_time_opened: pd.DataFrame, losses_by_time_opened: pd.DataFrame,
              equity: pd.Series, statistics: pd.Series,
              file_path: str, pdf_title = "", author = "", subject = "", keyworkds = ""):
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
    entris_bars_by_hour.plot.bar(ax=axes[0], color=entries_color)
    axes[0].set_title("Entries by Hour")
    axes[0].legend().remove()
    
    entris_bars_by_dow.plot.bar(ax=axes[1], color=entries_color)
    axes[1].set_title("Entries by Day Of Week")
    axes[1].legend().remove()
    
    entris_bars_by_month.plot.bar(ax=axes[2], color=entries_color)
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

    pdf_dict = pdf.infodict()
    if pdf_title != "":
      pdf_dict["Title"] = pdf_title
    if author != "":
      pdf_dict["Author"] = author
    if subject != "":
      pdf_dict["Subject"] = author
    if keyworkds != "":
      pdf_dict["Keywords"] = author
    pdf_dict["CreationDate"] = datetime.today()
    pdf_dict["ModificationDate"] = datetime.today()