import asyncio
from core.client import client

async def run():
    """
    Start the Telegram client and block until disconnected.
    """
    await client.start()
    print("[runner] Client started. Waiting for events...")
    await client.run_until_disconnected()

# Convenience for manual testing:
if __name__ == "__main__":
    asyncio.run(run())