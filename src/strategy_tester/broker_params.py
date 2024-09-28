class BrokerParams:
  """Class for Broker parameters"""
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
    Set initial balance.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert cash > 0, "cash should be greater then zero"
    self.__cash = cash
    return self

  def set_commission(self, commission: float):
    """
    Set the broker commission ratio.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert commission >= 0 and commission < 1.0, "commission should be greater or equal then 0 and lower then 1.0"
    self.__commission = commission
    return self
  
  def set_margin(self, margin: float):
    """
    Set the position margin.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert margin > 0 and margin <= 1.0, "margin should be between 0 and 1.0"
    self.__margin = margin
    return self
  
  def set_trade_on_close(self, trade_on_close: bool):
    """
    Set trade on close mode.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert type(trade_on_close) == bool, "trade_on_close should be bool"
    self.__trade_on_close = trade_on_close
    return self
  
  def set_hedging(self, hedging: bool):
    """
    Set hedging mode.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert type(hedging) == bool, "hedging should be bool"
    self.__hedging = hedging
    return self
  
  def set_exclusive_orders(self, exclusive_orders: bool):
    """
    Set exclusive orders mode.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
    """
    assert type(exclusive_orders) == bool, "exclusive_orders should be bool"
    self.__exclusive_orders = exclusive_orders
    return self
  
  def build(self) -> BrokerParams:
    """
    Return the broker params with the setted overrides.
    For full explanation see here <https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0>
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