from telethon import TelegramClient
from core.config import API_HASH, API_ID_INT, BOT_TOKEN

# Create and start a bot client only if BOT_TOKEN is provided; otherwise keep None.
bot = None
if BOT_TOKEN:
    try:
        # 'bot' session name will create a separate session file if needed
        bot = TelegramClient("bot", API_ID_INT, API_HASH)
        # Start the bot with the provided token
        bot.start(bot_token=BOT_TOKEN)
    except Exception as e:
        # If starting the bot fails, keep bot as None to avoid affecting the rest of the source
        print(f"[bot_client] Failed to start bot with BOT_TOKEN: {e}")
        bot = None