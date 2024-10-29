import collections
import os
from typing import Sequence

import pandas as pd

from ..utils.files import create_folder_if_not_exist


def save_dataframe_as_csv(data: pd.DataFrame,
                          directory: str,
                          filename: str,
                          reset_index: bool = False,
                          index_name: str = "",
                          save_index: bool = False,
                          columns: Sequence[collections.abc.Hashable] = []):
  """Save dataframe as csv
  
  `directory` Directory where to save the file\n

  `filename` File name\n

  `reset_index` If True reset the dataframe index before save it as csv\n

  `index_name` Desired new index name, usable if `reset_index` is True\n

  `save_index` If True preserve the index column

  `columns` (optional) Sequence of columns to save
  """
  if data.empty:
    return
  # print("save_dataframe_as_csv...")
  # print(data)
  create_folder_if_not_exist(directory)
  copied = data.copy()
  if reset_index:
    copied.reset_index(inplace=True)
    if index_name:
      copied.rename(columns={ "index": index_name }, inplace=True)
  file_path = os.path.join(directory, filename)
  # print(f"File path: {file_path}")
  # print(copied)
  columns = copied.columns if len(columns) == 0 else columns
  copied.to_csv(file_path, index=save_index, columns=columns)