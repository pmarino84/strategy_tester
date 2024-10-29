from backtesting import Strategy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ....utils.strategy_params import get_strategy_params


def _add_betterstrategyparams(pdf: PdfPages, strategy: Strategy, strategy_params_to_optimize: dict):
  if not isinstance(strategy, Strategy):
    return
  if strategy_params_to_optimize == None:
    return
  strategy_better_params = []
  for param_name, param_value in get_strategy_params(strategy).items():
    if param_name in strategy_params_to_optimize:
      strategy_better_params.append(f"{param_name}: {param_value}")
  strategy_better_params_str = "\n".join(strategy_better_params)
  text = f"Strategy better params:\n{strategy_better_params_str}"
  fig = plt.figure(figsize=(16, 8))
  fig.text(0.4, 0.6, text, size=16, ha="center")
  pdf.savefig()
  plt.close()