from telethon import TelegramClient
from telethon.sessions import StringSession

from core.config import API_HASH, STRING_SESSION, API_ID_INT

# Single shared TelegramClient instance for the whole app
client = TelegramClient(StringSession(STRING_SESSION), API_ID_INT, API_HASH)