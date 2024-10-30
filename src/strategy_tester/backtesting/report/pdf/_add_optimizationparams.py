from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ....backtesting.optimization_params import OptimizationParams

def _add_optimizationparams(pdf: PdfPages, params: OptimizationParams):
  if not isinstance(params, OptimizationParams):
    return
  fig = plt.figure(figsize=(16, 8))
  text = "Optimization params:"
  text += f"\nmaximize            = {params.maximize}"
  text += f"\nmethod              = {params.method}"
  text += f"\nmax_tries           = {params.max_tries}"
  text += f"\nreturn_heatmap      = {params.return_heatmap}"
  text += f"\nreturn_optimization = {params.return_optimization}"
  text += f"\nrandom_state        = {params.random_state}"
  fig.text(0.4, 0.6, text, size=16, ha="center")
  pdf.savefig()
  plt.close()