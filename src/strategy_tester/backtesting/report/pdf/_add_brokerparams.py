from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ....backtesting.broker_params import BrokerParams


def _add_brokerparams(pdf: PdfPages, params: BrokerParams):
  fig = plt.figure(figsize=(16, 8))
  text = "Broker params:"
  text += f"\ncash             = {params.cash}"
  text += f"\ncommission       = {params.commission}"
  text += f"\nmargin           = {params.margin}"
  text += f"\ntrades_on_close  = {params.trade_on_close}"
  text += f"\nhedging          = {params.hedging}"
  text += f"\nexclusive_orders = {params.exclusive_orders}"
  fig.text(0.4, 0.6, text, size=16, ha="center")
  pdf.savefig()
  plt.close()