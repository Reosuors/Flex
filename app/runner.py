import asyncio
import logging
from core.client import client
from core.bot_client import bot  # optional bot
from core.config import BOT_TOKEN

async def run():
    """
    Start the Telegram client(s) and block until disconnected.
    """
    tasks = []

    print("[runner] Attempting to start user client...")
    try:
        # Start user client
        await client.start()
        print("[runner] ✅ User client started successfully.")
        
        me = await client.get_me()
        print(f"[runner] Connected as: {me.first_name} (@{me.username if me.username else 'No Username'})")
    except Exception as e:
        print(f"[runner] ❌ Failed to start user client: {e}")
        return

    # Ensure log group is created on startup (best-effort)
    try:
        from core.error_reporting import ensure_log_group
        await ensure_log_group()
        print("[runner] Log group ensured.")
    except Exception as e:
        print(f"[runner] Log group error (non-critical): {e}")
        pass

    # Run plugin startup tasks (e.g., auto-join channels)
    try:
        from plugins import run_startup
        await run_startup()
        print("[runner] Plugin startup tasks completed.")
    except Exception as e:
        print(f"[runner] Plugin startup error: {e}")
        pass

    tasks.append(client.run_until_disconnected())

    # Start bot client if configured
    if bot is not None and BOT_TOKEN:
        try:
            await bot.start(bot_token=BOT_TOKEN)
            print("[runner] ✅ Bot client started.")
            tasks.append(bot.run_until_disconnected())
        except Exception as e:
            print(f"[runner] ❌ Failed to start bot client: {e}")
    else:
        print("[runner] BOT_TOKEN not set; interactive inline buttons will be limited.")

    # Wait until any disconnect
    print("[runner] Bot is now running and listening for commands...")
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run())
