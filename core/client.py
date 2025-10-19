from telethon import TelegramClient
from telethon.sessions import StringSession

from core.config import API_ID, API_HASH, STRING_SESSION

if not API_ID or not API_HASH or not STRING_SESSION:
    raise RuntimeError("Missing API_ID/API_HASH/STRING_SESSION in environment. Please set them in Render service settings.")

# Single shared TelegramClient instance for the whole app
client = TelegramClient(StringSession(STRING_SESSION), int(API_ID), API_HASH)