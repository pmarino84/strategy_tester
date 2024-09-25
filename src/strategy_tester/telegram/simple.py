from typing import Union
import requests
from telegram.error import TelegramError
# from .errors import TelegramError, HttpError
from .errors import HttpError

def find_telegram_chat_id(chat_title: str, bot_token: str):
  url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
  resp = requests.get(url).json()
  if not resp["ok"]:
    raise HttpError(resp["error_code"], resp["description"])
  result = resp["result"]
  list = []
  for item in result:
    if "my_chat_member" in item:
      if item["my_chat_member"]["chat"]["title"] == chat_title:
        list.append(item)
  
  if len(list) == 0:
    raise TelegramError(f"Failed to find chat id of `{chat_title}`")

  return list[-1]["my_chat_member"]["chat"]["id"]

def notify_telegram(chat_id: Union[int, str], bot_token: str, message: str):
  if type(chat_id) == str:
    chat_id = find_telegram_chat_id(chat_id, bot_token)
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
  resp = requests.get(url).json()
  if not resp["ok"]:
    print(resp)
    raise HttpError(resp["error_code"], resp["description"])
