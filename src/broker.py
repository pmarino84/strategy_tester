class BrokerParams:
  def __init__(
    self,
    cash: float = 10_000,
    commission: float = .0,
    margin: float = 1.,
    trade_on_close=False,
    hedging=False,
    exclusive_orders=False) -> None:
    self.cash = cash
    self.commission = commission
    self.margin = margin
    self.trade_on_close = trade_on_close
    self.hedging = hedging
    self.exclusive_orders = exclusive_orders

  def __str__(self) -> str:
    return f"<BrokerParams (cash={self.cash}, commission={self.commission}, margin={self.margin}, trade_on_close={self.trade_on_close}, hedging={self.hedging}, exclusive_orders={self.exclusive_orders})>"

class BrokerParamsBuilder:
  def __init__(self) -> None:
    self.__cash=10_000
    self.__commission=0.0
    self.__margin=1.0
    self.__trade_on_close=False
    self.__hedging=False
    self.__exclusive_orders=False
  
  def set_cash(self, cash):
    self.__cash = cash
    return self

  def set_commission(self, commission):
    self.__commission = commission
    return self
  
  def set_margin(self, margin):
    self.__margin = margin
    return self
  
  def set_trade_on_close(self, trade_on_close):
    self.__trade_on_close = trade_on_close
    return self
  
  def self_hedging(self, hedging):
    self.__hedging = hedging
    return self
  
  def self_exclusive_order(self, exclusive_order):
    self.__exclusive_orders = exclusive_order
    return self
  
  def build(self):
    return BrokerParams(
      cash=self.__cash,
      commission=self.__commission,
      margin=self.__margin,
      trade_on_close=self.__trade_on_close,
      hedging=self.__hedging,
      exclusive_orders=self.__exclusive_orders
    )