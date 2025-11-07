from telethon import TelegramClient
from core.config import API_HASH, API_ID_INT, BOT_TOKEN

# Create and start a bot client only if BOT_TOKEN is provided; otherwise keep None.
# Create a bot client only if BOT_TOKEN is provided; do not start it here.
bot = TelegramClient("bot", API_ID_INT, API_HASH) if BOT_TOKEN else None