import pandas as pd
import pandas_ta as ta
from backtesting import Strategy
from backtesting.lib import crossover

from ....strategy_tester.backtesting.broker_params import BrokerParams
from ....strategy_tester.backtesting.optimization_params import OptimizationParams
from ....strategy_tester.backtesting.pipeline.optimization import create_optimization_pipeline_with_metrics
from ....strategy_tester.pipeline import Context, Pipeline


def load_csv(file_path: str):
  data = pd.read_csv(file_path)
  return data

def format_gmt(gmt: str):
  gmt_pre = ""
  gmt_post = ""
  for i in range(len(gmt)):
      if i < 3:
          gmt_pre += gmt[i]
      else:
          gmt_post += gmt[i]
  return f"{gmt_pre}:{gmt_post}"

def apply_format_gmt(row: str):
  parts = row.split(" ")
  results = []
  for i in range(len(parts)):
    if "GMT" in parts[i]:
      gmt = parts[i].replace("GMT", "")
      gmt_formatted = format_gmt(gmt)
      results.append(f"GMT{gmt_formatted}")
    else:
      results.append(parts[i])
  return " ".join(results)

def process_forex_data(data: pd.DataFrame, datatime_column_name: str, datetime_format: str, is_utc: bool = False):
  data[datatime_column_name] = data[datatime_column_name].str.replace(".000", "")
  data[datatime_column_name] = data[datatime_column_name].apply(apply_format_gmt)

  data[datatime_column_name] = pd.to_datetime(data[datatime_column_name], format=datetime_format, utc=is_utc)
  data = data[data["High"] != data["Low"]]
  data.set_index(datatime_column_name, inplace=True)
  return data

def create_load_data(file_path: str, datatime_column_name: str, datetime_format: str, is_utc):
  def load_data(context: Context):
    data = load_csv(file_path)
    data = process_forex_data(data, datatime_column_name, datetime_format, is_utc)
    context.data = data
    return context
  return load_data

def create_strategy(context: Context):
  class ForexBollingerBandsSwing(Strategy):
    bb_period=20
    bb_stddev_multiplier=2.0
    # rsi_period=14
    # rsi_lower_threshold=30
    # rsi_higher_threshold=70
    atr_period=10
    sl_atr_multiplier=1.2
    tpsl_ratio=1.5
    risk_percent=0.01
    contract_size=100_000
    min_lot=0.01
    max_lot=100

    def init(self):
      super().init()
      self._min_lot_size = self.min_lot * self.contract_size
      self._max_lot_size = self.max_lot * self.contract_size

      bbands = ta.bbands(self.data["Close"].s, length=self.bb_period, std=self.bb_stddev_multiplier)
      self._lowerBollingerBand = self.I(lambda: bbands[bbands.columns[0]])
      # self._meanBollingerBand = self.I(lambda: bbands[bbands.columns[1]])
      self._upperBollingerBand = self.I(lambda: bbands[bbands.columns[2]])
      # self._bollingerBandWidth = self.I(lambda: bbands[bbands.columns[3]]) # BANDWIDTH = 100 * (UPPER - LOWER) / MID
      # self._bollingerBandPercent = self.I(lambda: bbands[bbands.columns[4]]) # PERCENT = (close - LOWER) / (UPPER - LOWER)

      # self._rsi = self.I(lambda: ta.rsi(self.data["Close"].s, length=self.rsi_period))
      self._atr = self.I(lambda: ta.atr(self.data["High"].s, self.data["Low"].s, self.data["Close"].s, length=self.atr_period))
    
    def calc_lot_size(self, close_price, sl_delta):
      decimal = 1e-2 if "JPY" in context.asset_name else 1e-4
      pip_value = (decimal / close_price) * 1e5
      lot_size = int((self.risk_percent * self.equity) / (sl_delta * pip_value)) # risk_amount / (sl_pips * pip_value) = position amount
      if lot_size < self._min_lot_size:
        lot_size = self._min_lot_size
      if lot_size > self._max_lot_size:
        lot_size = self._max_lot_size
      return lot_size

    def next(self):
      super().next()
      if len(self.trades) == 0:
        sl_delta = self._atr[-1] * self.sl_atr_multiplier
        close_price = self.data["Close"][-1]

        bb_long_signal = crossover(self.data["Close"], self._lowerBollingerBand)
        bb_short_signal = crossover(self._upperBollingerBand, self.data["Close"])

        lot_size = self.calc_lot_size(close_price, sl_delta)

        if bb_long_signal:
          sl = close_price - sl_delta
          tp = close_price + sl_delta * self.tpsl_ratio
          self.buy(sl=sl, tp=tp, size=lot_size)
        elif bb_short_signal:
          sl = close_price + sl_delta
          tp = close_price - sl_delta * self.tpsl_ratio
          self.sell(sl=sl, tp=tp, size=lot_size)

  context.strategy = ForexBollingerBandsSwing
  return context

def create_pipeline(
  asset_data: dict,
  broker_params: BrokerParams,
  optimization_params: OptimizationParams,
  telegram_bot_token: str,
  telegram_chat_id: str) -> Pipeline:
  data_loader = asset_data["data_loader"]
  data_file_path = data_loader["file_path"]
  datatime_column_name = data_loader["datatime_column_name"]
  datatime_format = data_loader["datatime_format"]
  return create_optimization_pipeline_with_metrics(
    {
      "sl_atr_multiplier": [i/10 for i in range(10, 21)],
      "tpsl_ratio": [i/10 for i in range(10, 21)],
    },
    create_load_data(data_file_path, datatime_column_name, datatime_format, data_loader["is_utc"]),
    create_strategy,
    asset_data["results_folder_path"],
    broker_params= broker_params,
    optimization_params=optimization_params,
    telegram_bot_token=telegram_bot_token,
    telegram_chat_id=telegram_chat_id)
