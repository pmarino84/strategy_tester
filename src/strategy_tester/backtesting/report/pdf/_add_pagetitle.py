from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def _add_pagetitle(pdf: PdfPages, strategy_name: str, asset_name: str):
  fig = plt.figure(figsize=(16, 16))
  fig.text(0.5, 0.6, strategy_name, size=24, ha="center")
  fig.text(0.5, 0.5, asset_name, size=18, ha="center")
  pdf.savefig()
  plt.close()