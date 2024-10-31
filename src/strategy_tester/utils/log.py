def log(message: str, strategy_name: str = "N/A", asset_name: str = "N/A", level: str = "INFO"):
  prefix = f"Level='{level}'; "
  if strategy_name != "N/A":
    prefix += f"Strategy='{strategy_name}'; "
  if asset_name != "N/A":
    prefix += f"Asset='{asset_name}'; "
  print(f"{prefix} Message='{message}'")