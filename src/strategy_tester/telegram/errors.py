# class TelegramError(Exception):
#   def __init__(self, *args: object) -> None:
#     super().__init__(*args)

# class HttpError(TelegramError):
class HttpError(Exception):
  def __init__(self, error_code: int, description: str, *args: object) -> None:
    self.error_code = error_code
    self.error_description = description
    super().__init__(*args)
