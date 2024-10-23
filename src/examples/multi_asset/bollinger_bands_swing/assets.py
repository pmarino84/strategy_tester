from os import getcwd

PARENT_FOLDER = f"{getcwd()}/src/examples/multi_asset/bollinger_bands_swing"

assets = {}

assets["AUDUSD"] = {}
assets["AUDUSD"]["data_loader"] = {}
assets["AUDUSD"]["data_loader"]["file_path"] = f"{PARENT_FOLDER}/data/AUDUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["AUDUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["AUDUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["AUDUSD"]["data_loader"]["is_utc"] = True
assets["AUDUSD"]["results_folder_path"] = f"{PARENT_FOLDER}/results/AUDUSD/optimization"

assets["EURUSD"] = {}
assets["EURUSD"]["data_loader"] = {}
assets["EURUSD"]["data_loader"]["file_path"] = f"{PARENT_FOLDER}/data/EURUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["EURUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["EURUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["EURUSD"]["data_loader"]["is_utc"] = True
assets["EURUSD"]["results_folder_path"] = f"{PARENT_FOLDER}/results/EURUSD/optimization"
