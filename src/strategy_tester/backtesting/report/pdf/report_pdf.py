from matplotlib.backends.backend_pdf import PdfPages

from ....pipeline.context import Context
from ._add_betterstrategyparams import _add_betterstrategyparams
from ._add_brokerparams import _add_brokerparams
from ._add_equity import _add_equity
from ._add_heatmap import _add_heatmap
from ._add_metadata import _add_metadata
from ._add_metrics import _add_metrics
from ._add_optimizationparams import _add_optimizationparams
from ._add_pagetitle import _add_pagetitle
from ._add_pnl_distribution import _add_pnl_distribution
from ._add_statistics import _add_statistics


# TODO: BEAUTIFY THE NEW PAGES!!!!!
def report_to_pdf(context: Context, pdf_title = "", author = "", subject = "", keyworkds = ""):
  """
  Save backtest/optimization pipeline result as pdf report.

  `context` pipeline result context.\n
  
  `pdf_title` (optional) pdf title metadata.\n
  `author` (optional) pdf Author metadata.\n
  `subject` (optional) pdf Subject metadata.\n
  `keywords` (optional) pdf Keywords metadata.\n
  """
  statistics = context.stats

  if statistics.empty:
    # if there isn't statistics data also there isn't metrics, equity, heatmap...
    return

  file_path = f"{context.result_folder}/report.pdf"
  with PdfPages(file_path) as pdf:
    _add_pagetitle(pdf, context.strategy_name or context.strategy.__name__, context.asset_name)

    _add_statistics(pdf, statistics)

    _add_betterstrategyparams(pdf, statistics["_strategy"], context.strategy_params_to_optimize)

    _add_optimizationparams(pdf, context.optimization_params)

    _add_brokerparams(pdf, context.broker_params)

    _add_equity(pdf, statistics["_equity_curve"]["Equity"])

    _add_metrics(pdf, context.metrics)

    _add_pnl_distribution(pdf, statistics["_trades"]["PnL"], bins=100)

    _add_heatmap(pdf, context.heatmap)

    _add_metadata(pdf, pdf_title, author, subject, keyworkds)
