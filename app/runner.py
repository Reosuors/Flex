import asyncio
from core.client import client
from core.bot_client import bot_client
from core.config import BOT_TOKEN


async def run():
    """
    Start the Telegram user client, and optional bot client if BOT_TOKEN is set.
    Run both until disconnected.
    """
    await client.start()
    print("[runner] User client started.")

    tasks = [asyncio.create_task(client.run_until_disconnected())]

    if bot_client:
        # start bot with token
        await bot_client.start(bot_token=BOT_TOKEN)
        print("[runner] Bot client started.")
        tasks.append(asyncio.create_task(bot_client.run_until_disconnected()))

    print("[runner] Waiting for events...")
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

# Convenience for manual testing:
if __name__ == "__main__":
    asyncio.run(run())