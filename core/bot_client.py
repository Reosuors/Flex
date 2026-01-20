from telethon import TelegramClient
import logging
from core.config import API_HASH, API_ID_INT, BOT_TOKEN

# Create and start a bot client only if BOT_TOKEN is provided; otherwise keep None.
# Create a bot client only if BOT_TOKEN is provided; do not start it here.
bot = None
if BOT_TOKEN:
    try:
        bot = TelegramClient("bot", API_ID_INT, API_HASH)
        logging.info("[bot] Assistant bot client initialized (BOT_TOKEN provided).")
    except Exception as e:
        logging.error(f"[bot] Failed to initialize bot client: {e}")
        bot = None
else:
    logging.info("[bot] No BOT_TOKEN provided. Inline buttons and assistant bot will be disabled.")
