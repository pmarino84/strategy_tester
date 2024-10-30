from backtesting import Strategy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ....backtesting.broker_params import BrokerParams
from ....backtesting.optimization_params import OptimizationParams
from ....utils.strategy_params import get_strategy_params


def _better_strategy_params_as_text(strategy: Strategy, strategy_params_to_optimize: dict):
  if not isinstance(strategy, Strategy):
    return ""
  if strategy_params_to_optimize == None:
    return ""
  strategy_better_params = []
  for param_name, param_value in get_strategy_params(strategy).items():
    if param_name in strategy_params_to_optimize:
      strategy_better_params.append(f"{param_name}: {param_value}")
  strategy_better_params_str = "\n".join(strategy_better_params)
  return f"Strategy better params:\n{strategy_better_params_str}"

def _optimization_params_as_text(params: OptimizationParams):
  if not isinstance(params, OptimizationParams):
    return ""
  text = "Optimization params:"
  text += f"\nmaximize            = {params.maximize}"
  text += f"\nmethod              = {params.method}"
  text += f"\nmax_tries           = {params.max_tries}"
  text += f"\nreturn_heatmap      = {params.return_heatmap}"
  text += f"\nreturn_optimization = {params.return_optimization}"
  text += f"\nrandom_state        = {params.random_state}"
  return text

def _brokerparams_as_text(params: BrokerParams):
  text = "Broker params:"
  text += f"\ncash             = {params.cash}"
  text += f"\ncommission       = {params.commission}"
  text += f"\nmargin           = {params.margin}"
  text += f"\ntrades_on_close  = {params.trade_on_close}"
  text += f"\nhedging          = {params.hedging}"
  text += f"\nexclusive_orders = {params.exclusive_orders}"
  return text

# TODO: provare ad usare questo metodo per allineare meglio i testi
# https://matplotlib.org/stable/gallery/text_labels_and_annotations/fancyarrow_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancyarrow-demo-py
def _add_params(pdf: PdfPages, strategy: Strategy, strategy_params_to_optimize: dict, optimization_params: OptimizationParams, broker_params: BrokerParams) -> None:
  betters_strategy_params_txt = _better_strategy_params_as_text(strategy, strategy_params_to_optimize)
  optimization_params_txt = _optimization_params_as_text(optimization_params)
  broker_params_txt = _brokerparams_as_text(broker_params)

  if betters_strategy_params_txt == "" or optimization_params_txt == "":
    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, 0.6, broker_params_txt, size=16, ha="center")
    pdf.savefig()
    plt.close()
    return

  fig, axes = plt.subplots(1, 2, figsize=(16, 8))
  for ax in axes.flat:
    ax.set_axis_off()
  axes[0].text(0.5, 0.5, betters_strategy_params_txt, size=16, ha="center")
  axes[1].text(0.5, 0.5, optimization_params_txt + "\n\n" + broker_params_txt, size=16, ha="center")
  # fig.subplots_adjust(hspace=0.8)
  pdf.savefig(fig)
  plt.close()