from typing import Optional, Union

import pandas as pd

def test_optional(data: Optional[Union[pd.DataFrame, pd.Series]] = None) -> None:
  if isinstance(data, (pd.DataFrame, pd.Series)):
    if data.empty:
      print("EMPTY")
      return
    print(data)
    return
  print("NONEEEE")

test_optional()
test_optional(pd.DataFrame())
test_optional(pd.DataFrame({ "A": ["1"], "B": ["2"], "C": ["3"] }))
test_optional(pd.Series())

def is_available(data: Optional[Union[pd.DataFrame, pd.Series]]) -> bool:
  if isinstance(data, (pd.DataFrame, pd.Series)):
    return not data.empty
  if data == None:
    return False
  return True

def test_optional_v2(data: Optional[Union[pd.DataFrame, pd.Series]] = None) -> None:
  if not is_available(data):
    print("Empty | None data")
    return
  print(data)


test_optional_v2()
test_optional_v2(pd.DataFrame())
test_optional_v2(pd.DataFrame({ "1": ["a"], "2": ["b"], "3": ["c"] }))
test_optional_v2(pd.Series())