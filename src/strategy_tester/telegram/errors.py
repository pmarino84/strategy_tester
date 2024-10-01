# class TelegramError(Exception):
#   def __init__(self, *args: object) -> None:
#     super().__init__(*args)

# class HttpError(TelegramError):
class HttpError(Exception):
  """
  Http error used by `.simple.notify_telegram` when there is an error response
  """
  def __init__(self, error_code: int, description: str, *args: object) -> None:
    self.error_code = error_code
    """Http response error code"""
    self.error_description = description
    """Response error description"""
    super().__init__(*args)
