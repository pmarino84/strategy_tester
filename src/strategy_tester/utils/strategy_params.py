from backtesting import Strategy


def get_strategy_params(strategy: Strategy) -> dict:
  """Return a dictionary containing only the strategy params defined by you"""
  params = {}
  for key, value in vars(strategy).items():
    if not callable(value) and not key.startswith("__") and not key.startswith("_"):
      params[key] = value
  return params