import pytest

from strategy_tester.backtesting.optimization_params import OptimizationParams, OptimizationParamsBuilder


def assert_params_equal(first: OptimizationParams, second: OptimizationParams):
  if first.maximize != second.maximize:
    return False
  
  if first.method != second.method:
    return False
  
  if first.max_tries != second.max_tries:
    return False
  
  if first.constraint != second.constraint:
    return False
  
  if first.return_heatmap != second.return_heatmap:
    return False
  
  if first.return_optimization != second.return_optimization:
    return False
  
  if first.random_state != second.random_state:
    return False
  
  return True

def test_set_default_params():
  def_params = OptimizationParams(return_heatmap=True)
  params = OptimizationParamsBuilder().build()
  assert assert_params_equal(def_params, params)

def test_set_maximize_to_return_pct():
  assert OptimizationParamsBuilder().set_maximize("Return [%]").build().maximize == "Return [%]"

def test_set_method_raise_value_error():
  with pytest.raises(ValueError):
    OptimizationParamsBuilder().set_method("bbb")

def test_set_method_set_to_skopt():
  assert OptimizationParamsBuilder().set_method("skopt").build().method == "skopt"

def test_set_max_tries_raise_value_error():
  with pytest.raises(ValueError):
    OptimizationParamsBuilder().set_max_tries(0)

def test_set_max_tries_to_1000():
  assert OptimizationParamsBuilder().set_max_tries(1000).build().max_tries == 1000

def test_set_constraint():
  constraint = lambda x: True
  assert OptimizationParamsBuilder().set_constraint(constraint).build().constraint == constraint

def test_set_return_heatmap_to_false():
  assert OptimizationParamsBuilder().set_return_heatmap(False).build().return_heatmap == False

def test_set_return_optimization_to_true():
  assert OptimizationParamsBuilder().set_return_optimization(True).build().return_optimization == True

def test_set_random_state_to_one():
  assert OptimizationParamsBuilder().set_random_state(1).build().random_state == 1