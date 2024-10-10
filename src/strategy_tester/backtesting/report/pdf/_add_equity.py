import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _add_equity(pdf: PdfPages, equity: pd.Series):
  if not equity.empty:
    plt.figure(figsize=(16, 8))
    equity.plot.line()
    plt.title("Equity")
    pdf.savefig()
    plt.close()