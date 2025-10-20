from telethon import TelegramClient
from core.config import API_ID, API_HASH, BOT_TOKEN

# Optional bot client. Only created if BOT_TOKEN present.
bot_client = None
if API_ID and API_HASH and BOT_TOKEN:
    # Named session 'bot' (file-based). On ephemeral FS it's fine.
    bot_client = TelegramClient("bot", int(API_ID), API_HASH)