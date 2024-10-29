import os

def create_file_suffix(suffix = ""):
  return "" if suffix == "" else f"_{suffix}"

def create_folder_if_not_exist(folder_path: str):
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)