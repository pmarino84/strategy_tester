import pytest

from ...metrics.utils import assert_offset_values, resample_offset_to_field_name

def test_assert_offset_values_rais_error():
  with pytest.raises(ValueError):
    assert_offset_values('P')

# https://stackoverflow.com/questions/20274987/how-to-use-pytest-to-check-that-error-is-not-raised
def test_assert_offset_values():
  offset = "M"
  try:
    assert_offset_values(offset)
  except ValueError:
    pytest.fail(f"offset must be one of H, D, M not {offset}")

def test_resample_offset_to_field_name_hour():
  assert resample_offset_to_field_name("H") == "hour"

def test_resample_offset_to_field_name_day_of_week():
  assert resample_offset_to_field_name("D") == "day_of_week"

def test_resample_offset_to_field_name_month():
  assert resample_offset_to_field_name("M") == "month"