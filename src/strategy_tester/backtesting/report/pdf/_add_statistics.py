import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _add_statistics(pdf: PdfPages, statistics: pd.Series):
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