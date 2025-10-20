import asyncio
from core.client import client
from core.bot_client import bot  # optional bot

async def run():
    """
    Start the Telegram client(s) and block until disconnected.
    """
    tasks = []

    # Start user client
    await client.start()
    print("[runner] User client started.")
    tasks.append(client.run_until_disconnected())

    # Start bot client if configured
    if bot is not None:
        await bot.start(bot_token=True)  # start with bot token already bound in core.bot_client
        print("[runner] Bot client started.")
        tasks.append(bot.run_until_disconnected())
    else:
        print("[runner] BOT_TOKEN not set; interactive inline buttons will be limited.")

    # Wait until any disconnect
    await asyncio.gather(*tasks)

# Convenience for manual testing:
if __name__ == "__main__":
    asyncio.run(run())