from typing import Callable, Union

import pandas as pd

class OptimizationParams:
  """
  Class for Optimization process params.
  
  `maximize` is a string key from the
  `backtesting.backtesting.Backtest.run`-returned results series,
  or a function that accepts this series object and returns a number;
  the higher the better. By default, the method maximizes
  Van Tharp's [System Quality Number](https://google.com/search?q=System+Quality+Number).
  
  `method` is the optimization method. Currently two methods are supported:

  * `"grid"` which does an exhaustive (or randomized) search over the
    cartesian product of parameter combinations, and
  * `"skopt"` which finds close-to-optimal strategy parameters using
    [model-based optimization], making at most `max_tries` evaluations.

  [model-based optimization]: https://scikit-optimize.github.io/stable/auto_examples/bayesian-optimization.html

  `max_tries` is the maximal number of strategy runs to perform.
  If `method="grid"`, this results in randomized grid search.
  If `max_tries` is a floating value between (0, 1], this sets the
  number of runs to approximately that fraction of full grid space.
  Alternatively, if integer, it denotes the absolute maximum number
  of evaluations. If unspecified (default), grid search is exhaustive,
  whereas for `method="skopt"`, `max_tries` is set to 200.

  `constraint` is a function that accepts a dict-like object of
  parameters (with values) and returns `True` when the combination
  is admissible to test with. By default, any parameters combination
  is considered admissible.

  If `return_heatmap` is `True`, besides returning the result
  series, an additional `pd.Series` is returned with a multiindex
  of all admissible parameter combinations, which can be further
  inspected or projected onto 2D to plot a heatmap
  (see `backtesting.lib.plot_heatmaps()`).

  If `return_optimization` is True and `method = 'skopt'`,
  in addition to result series (and maybe heatmap), return raw
  [`scipy.optimize.OptimizeResult`][OptimizeResult] for further
  inspection, e.g. with [scikit-optimize]\
  [plotting tools].

  [OptimizeResult]: \
      https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html
  [scikit-optimize]: https://scikit-optimize.github.io
  [plotting tools]: https://scikit-optimize.github.io/stable/modules/plots.html

  If you want reproducible optimization results, set `random_state`
  to a fixed integer random seed.
  """
  def __init__(
    self,
    maximize: Union[str, Callable[[pd.Series], float]] = 'SQN',
    method: str = 'grid',
    max_tries: Union[int, float] = None,
    constraint: Callable[[dict], bool] = None,
    return_heatmap: bool = False,
    return_optimization: bool = False,
    random_state: int = None) -> None:
    self.maximize = maximize
    self.method = method
    self.max_tries = max_tries
    self.constraint = constraint
    self.return_heatmap = return_heatmap
    self.return_optimization = return_optimization
    self.random_state = random_state

class OptimizationParamsBuilder:
  """Optimization params builder"""
  def __init__(self) -> None:
    self.reset()
  
  def reset(self) -> None:
    """Reset to it's initial value the builder attributes"""
    self.__maximize = "SQN"
    self.__method = "grid"
    self.__max_tries = None
    self.__constraint = None
    self.__return_heatmap = True
    self.__return_optimization = False
    self.__random_state = None
  
  def set_maximize(self, maximize: Union[str, Callable[[pd.Series], float]]):
    self.__maximize = maximize
    return self
  
  def set_method(self, method: str):
    if method not in ["grid", "skopt"]:
      raise ValueError(f"method should be 'grid' or 'skopt'")
    self.__method = method
    return self
  
  def set_max_tries(self, max_tries: Union[int, float]):
    if max_tries <= 0:
      raise ValueError(F"max_tries should be greater then zero")
    self.__max_tries = max_tries
    return self
  
  def set_constraint(self, constraint: Callable[[dict], bool]):
    self.__constraint = constraint
    return self
  
  def set_return_heatmap(self, return_heatmap: bool):
    self.__return_heatmap = return_heatmap
    return self
  
  def set_return_optimization(self, return_optimization: bool):
    self.__return_optimization = return_optimization
    return self
  
  def set_random_state(self, random_state: int):
    self.__random_state = random_state
    return self
  
  def build(self) -> OptimizationParams:
    """
    Return the optimization params with the setted overrides. See `OptimizationParams`.
    """
    params = OptimizationParams(
      self.__maximize,
      self.__method,
      self.__max_tries,
      self.__constraint,
      self.__return_heatmap,
      self.__return_optimization,
      self.__random_state)
    self.reset()
    return params