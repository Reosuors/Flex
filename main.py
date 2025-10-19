import asyncio

from core.client import client
from plugins import load_all


async def main():
    # Load all plugins (handlers will attach to the shared client)
    load_all()

    # Start client and block
    await client.start()
    print("[main] Client started. Waiting for events...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass