import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _add_pnl_distribution(pdf: PdfPages, pnl: pd.Series, bins: int = 10):
  plt.figure(figsize=(16, 8))
  pnl.hist(bins=bins)
  plt.title("PnL Distribution")
  pdf.savefig()
  plt.close()