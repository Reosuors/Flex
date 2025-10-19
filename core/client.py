from telethon import TelegramClient
from telethon.sessions import StringSession

from core.config import API_ID, API_HASH, STRING_SESSION

# Single shared TelegramClient instance for the whole app
client = TelegramClient(StringSession(STRING_SESSION), int(API_ID), API_HASH)