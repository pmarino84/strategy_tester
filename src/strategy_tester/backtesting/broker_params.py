class BrokerParams:
  """
  Class to simplify Broker parameters configuration.

  `cash` Initial account cash.\n
  `commission` The commission ratio.\nE.g.: if your broker commission is 1% of trade value set commission to 0.01.\n
  `margin` Required margin for a leveraged account.\nTo run the backtest using e.g. 50:1 leverge that your broker allows, set margin to 0.02 (1 / leverage).\n
  `trades_on_close` If trade_on_close is True, market orders will be filled with respect to the current bar's closing price instead of the next bar's open.\n
  `hedging` If hedging is True, allow trades in both directions simultaneously. If False, the opposite-facing orders first close existing trades.\n
  `exclusive_orders` If exclusive_orders is True, each new order auto-closes the previous trade/position, making at most a single trade (long or short) in effect at each time.\n
  """
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
  """Broker params builder"""
  def __init__(self) -> None:
    self.reset()

  def reset(self) -> None:
    """Reset to it's initial value the builder attributes"""
    self.__cash=10_000
    self.__commission=0.0
    self.__margin=1.0
    self.__trade_on_close=False
    self.__hedging=False
    self.__exclusive_orders=False
  
  def set_cash(self, cash: float):
    """
    Set initial account balance.
    """
    assert cash > 0, "cash should be greater then zero"
    self.__cash = cash
    return self

  def set_commission(self, commission: float):
    """
    Set the broker commission ratio. See `BrokerParams.commission`.
    """
    assert commission >= 0 and commission < 1.0, "commission should be greater or equal then 0 and lower then 1.0"
    self.__commission = commission
    return self
  
  def set_margin(self, margin: float):
    """
    Set the position margin. See `BrokerParams.margin`.
    """
    assert margin > 0 and margin <= 1.0, "margin should be between 0 and 1.0"
    self.__margin = margin
    return self
  
  def set_trade_on_close(self, trade_on_close: bool):
    """
    Set trade on close mode. See `BrokerParams.trade_on_close`.
    """
    assert type(trade_on_close) == bool, "trade_on_close should be bool"
    self.__trade_on_close = trade_on_close
    return self
  
  def set_hedging(self, hedging: bool):
    """
    Set hedging mode. See `BrokerParams.hedging`.
    """
    assert type(hedging) == bool, "hedging should be bool"
    self.__hedging = hedging
    return self
  
  def set_exclusive_orders(self, exclusive_orders: bool):
    """
    Set exclusive orders mode. See `BrokerParams.exclusive_orders`.
    """
    assert type(exclusive_orders) == bool, "exclusive_orders should be bool"
    self.__exclusive_orders = exclusive_orders
    return self
  
  def build(self) -> BrokerParams:
    """
    Return the broker params with the setted overrides. See `BrokerParams`.
    """
    params = BrokerParams(
      cash=self.__cash,
      commission=self.__commission,
      margin=self.__margin,
      trade_on_close=self.__trade_on_close,
      hedging=self.__hedging,
      exclusive_orders=self.__exclusive_orders
    )
    self.reset()
    return params