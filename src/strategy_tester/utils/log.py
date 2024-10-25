from ..pipeline.context import Context


def log(context: Context, message: str, level: str = "INFO"):
  asset_name = context.asset_name or "N/A"
  strategy_name = context.strategy_name or (context.strategy and context.strategy.__name__ )or "N/A"
  prefix = f"Level='{level}'; "
  if strategy_name != "N/A":
    prefix += f"Strategy='{strategy_name}'; "
  if asset_name != "N/A":
    prefix += f"Asset='{asset_name}'; "
  print(f"{prefix} Message='{message}'")