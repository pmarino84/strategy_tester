from backtesting import Strategy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ....backtesting.broker_params import BrokerParams
from ....backtesting.optimization_params import OptimizationParams
from ....utils.strategy_params import get_strategy_params

def _better_strategy_params_to_list(strategy: Strategy, strategy_params_to_optimize: dict):
  if not isinstance(strategy, Strategy):
    return []
  if strategy_params_to_optimize == None:
    return []
  strategy_better_params = []
  for param_name, param_value in get_strategy_params(strategy).items():
    if param_name in strategy_params_to_optimize:
      strategy_better_params.append(f"{param_name}: {param_value}")
  return strategy_better_params

def _optimization_params_to_list(params: OptimizationParams):
  if not isinstance(params, OptimizationParams):
    return []
  return params.to_text_list()

def _show_only_broker_params(pdf: PdfPages, broker_param_list: list[str]):
  rows = ["Broker params:"] + broker_param_list

  ncol = 1
  nrow = 1

  row_offset = .005
  row_height = .015 # 1.0 / max_row_count

  axes = plt.figure(figsize=(21, 29.7)).add_gridspec(nrow, ncol, wspace=.2, left=0.05, right=.95, bottom=.05, top=.95).subplots() # A4 inches

  axes.set_axis_off()

  for i, text in enumerate(rows):
    y = 1 - i * row_height - row_offset
    fontweight = "bold" if text in ["Broker params:"] else "normal"
    axes.text(0, y, text, transform=axes.transAxes, size="large", horizontalalignment="left", verticalalignment="center", fontweight=fontweight)
  
  pdf.savefig()
  plt.close()

def _show_all_params(pdf: PdfPages, better_strategy_param_list: list[str], optimization_param_list: list[str], broker_param_list: list[str]):
  left_rows  = ["Better strategy params:"] + better_strategy_param_list
  right_rows = ["Optimization params:"] + optimization_param_list + ["Broker params:"] + broker_param_list

  # max_row_count = max(len(left_rows), len(right_rows))

  ncol = 2
  nrow = 1

  row_offset = .005
  row_height = .015 # 1.0 / max_row_count

  axes = plt.figure(figsize=(21, 29.7)).add_gridspec(nrow, ncol, wspace=.2, left=0.05, right=.95, bottom=.05, top=.95).subplots() # A4 inches

  for ax in axes.flat:
    ax.set_axis_off()

  (ax1, ax2) = axes

  for i, text in enumerate(left_rows):
    y = 1 - i * row_height - row_offset
    fontweight = "bold" if text in ["Better strategy params:"] else "normal"
    ax1.text(0, y, text, transform=ax1.transAxes, size="large", horizontalalignment="left", verticalalignment="center", fontweight=fontweight)

  for i, text in enumerate(right_rows):
    y = 1 - i * row_height - row_offset
    fontweight = "bold" if text in ["Optimization params:", "Broker params:"] else "normal"
    ax2.text(0, y, text, transform=ax2.transAxes, size="large", horizontalalignment="left", verticalalignment="center", fontweight=fontweight)
  
  pdf.savefig()
  plt.close()

# https://matplotlib.org/stable/gallery/text_labels_and_annotations/fancyarrow_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancyarrow-demo-py
# https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
def _add_params(pdf: PdfPages, strategy: Strategy, strategy_params_to_optimize: dict, optimization_params: OptimizationParams, broker_params: BrokerParams) -> None:
  better_strategy_param_list = _better_strategy_params_to_list(strategy, strategy_params_to_optimize)
  optimization_param_list    = _optimization_params_to_list(optimization_params)
  broker_param_list          = broker_params.to_text_list()

  if len(better_strategy_param_list) == 0:
    _show_only_broker_params(pdf, broker_param_list)
  else:
    _show_all_params(pdf, better_strategy_param_list, optimization_param_list, broker_param_list)