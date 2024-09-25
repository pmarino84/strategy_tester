def assert_offset_values(offset: str):
  if offset not in ["H", "D", "M"]:
    raise ValueError(f"offset must be one of H, D, M not {offset}")

def resample_offset_to_field_name(offset: str):
  if offset == "H":
    return "hour"
  if offset == "D":
    return "day_of_week"
  return "month"
