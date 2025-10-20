from telethon import TelegramClient
from core.config import API_HASH, API_ID_INT, BOT_TOKEN

# Create a bot client only if BOT_TOKEN is provided
bot = None
if BOT_TOKEN:
    # 'bot' session name will create a separate session file if needed
    bot = TelegramClient("bot", API_ID_INT, API_HASH)