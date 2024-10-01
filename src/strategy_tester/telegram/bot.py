from typing import Union
from telegram import Bot, InputFile
from telegram.error import TelegramError
# from .errors import TelegramError

class TelegramBot:
  """Telegram bot class to communicate with your desired chat"""
  def __init__(self, token: str) -> None:
    self.bot = Bot(token=token)
    """python-telegram-bot Bot instance"""
  
  async def send_message(self, chat_id: Union[int, str], text: str):
    """send the message to the chat with the given chat id"""
    try:
      await self.bot.send_message(chat_id=chat_id, text=text)
      # print(f"Message `{text}`successfully sent to chat {chat_id}")
      print(f"Message successfully sent to chat {chat_id}")
    except Exception as ex:
      # print(f"Failed to send message `{text}` to chat {chat_id}: {ex}")
      raise TelegramError(f"Failed to send message `{text}` to chat {chat_id}")
  
  async def send_document(self, chat_id: Union[int, str], file_path: str):
    """send the document at file path to the chat with the given chat id"""
    try:
      with open(file_path, "rb") as file:
        await self.bot.send_document(chat_id=chat_id, document=InputFile(file))
      print(f"Document `{file_path}` successfully sent to chat {chat_id}")
    except Exception as ex:
      # print(f"Failed to send document `{file_path}` to chat {chat_id}: {ex}")
      raise TelegramError(f"Failed to send document `{file_path}` to chat {chat_id}")

  async def get_chat_id_by_chat_title(self, chat_title: str) -> int:
    try:
      updates = await self.bot.get_updates()
      filtered = []
      for update in updates:
        if update.my_chat_member:
          chat = update.my_chat_member.chat
          if chat.title == chat_title:
            filtered.append(chat)
      
      if len(filtered) == 0:
        raise TelegramError(f"Chat id for `{chat_title}` not found")
      
      chat_id = filtered[-1].id
      print(chat_id)
      return chat_id
    except Exception as ex:
      raise TelegramError(f"Failed to find chat id of `{chat_title}`")
