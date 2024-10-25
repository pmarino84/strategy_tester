import pytest

from strategy_tester.backtesting.broker_params import BrokerParamsBuilder


def test_set_cash_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_cash(0)

def test_set_cash():
  assert BrokerParamsBuilder().set_cash(2_000).build().cash == 2_000

def test_set_commission_lower_then_zero_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_commission(-1)

def test_set_commission_equal_to_one_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_commission(1)

def test_set_commission():
  assert BrokerParamsBuilder().set_commission(0.02).build().commission == 0.02

def test_set_margin_as_zero_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_margin(0)

def test_set_margin_greater_then_one_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_margin(10)

def test_set_margin():
  assert BrokerParamsBuilder().set_margin(1/10).build().margin == 1/10

def test_set_trade_on_close_as_not_bool_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_trade_on_close(3)

def test_set_trade_on_close():
  assert BrokerParamsBuilder().set_trade_on_close(True).build().trade_on_close

def test_set_hedging_as_not_bool_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_hedging(3)

def test_set_hedging():
  assert BrokerParamsBuilder().set_hedging(True).build().hedging

def test_set_exclusive_orders_as_not_bool_raise_error():
  with pytest.raises(Exception):
    BrokerParamsBuilder().set_exclusive_orders(3)

def test_set_exclusive_orders():
  assert BrokerParamsBuilder().set_exclusive_orders(True).build().exclusive_orders