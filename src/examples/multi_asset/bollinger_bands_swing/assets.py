from os import getcwd

DATA_PARENT_FOLDER = f"{getcwd()}/src/examples/data/forex"
RESULTS_PARENT_FOLDER = f"{getcwd()}/src/examples/multi_asset/bollinger_bands_swing"

assets = {}

assets["AUDUSD"] = {}
assets["AUDUSD"]["data_loader"] = {}
assets["AUDUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/AUDUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["AUDUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["AUDUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["AUDUSD"]["data_loader"]["is_utc"] = True
assets["AUDUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/AUDUSD/optimization"

assets["EURUSD"] = {}
assets["EURUSD"]["data_loader"] = {}
assets["EURUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/EURUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["EURUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["EURUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["EURUSD"]["data_loader"]["is_utc"] = True
assets["EURUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/EURUSD/optimization"

assets["GBPUSD"] = {}
assets["GBPUSD"]["data_loader"] = {}
assets["GBPUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/GBPUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["GBPUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["GBPUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["GBPUSD"]["data_loader"]["is_utc"] = True
assets["GBPUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/GBPUSD/optimization"

assets["NZDUSD"] = {}
assets["NZDUSD"]["data_loader"] = {}
assets["NZDUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/NZDUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["NZDUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["NZDUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["NZDUSD"]["data_loader"]["is_utc"] = True
assets["NZDUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/NZDUSD/optimization"

assets["USDCAD"] = {}
assets["USDCAD"]["data_loader"] = {}
assets["USDCAD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/USDCAD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["USDCAD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["USDCAD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["USDCAD"]["data_loader"]["is_utc"] = True
assets["USDCAD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/USDCAD/optimization"

assets["USDCHF"] = {}
assets["USDCHF"]["data_loader"] = {}
assets["USDCHF"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/USDCHF_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["USDCHF"]["data_loader"]["datatime_column_name"] = "Local time"
assets["USDCHF"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["USDCHF"]["data_loader"]["is_utc"] = True
assets["USDCHF"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/USDCHF/optimization"

assets["USDJPY"] = {}
assets["USDJPY"]["data_loader"] = {}
assets["USDJPY"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/USDJPY_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["USDJPY"]["data_loader"]["datatime_column_name"] = "Local time"
assets["USDJPY"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["USDJPY"]["data_loader"]["is_utc"] = True
assets["USDJPY"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/USDJPY/optimization"

assets["XAGUSD"] = {}
assets["XAGUSD"]["data_loader"] = {}
assets["XAGUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/XAGUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["XAGUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["XAGUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["XAGUSD"]["data_loader"]["is_utc"] = True
assets["XAGUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/XAGUSD/optimization"

assets["XAUUSD"] = {}
assets["XAUUSD"]["data_loader"] = {}
assets["XAUUSD"]["data_loader"]["file_path"] = f"{DATA_PARENT_FOLDER}/XAUUSD_Candlestick_5_M_BID_01.01.2019-31.12.2021.csv"
assets["XAUUSD"]["data_loader"]["datatime_column_name"] = "Local time"
assets["XAUUSD"]["data_loader"]["datatime_format"] = "%d.%m.%Y %H:%M:%S GMT%z"
assets["XAUUSD"]["data_loader"]["is_utc"] = True
assets["XAUUSD"]["results_folder_path"] = f"{RESULTS_PARENT_FOLDER}/results/XAUUSD/optimization"