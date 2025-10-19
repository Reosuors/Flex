import asyncio

from app.loader import load_plugins
from app.runner import run as run_client


async def main():
    # Load all plugins (handlers will attach to the shared client)
    load_plugins()

    # Start client and block
    await run_client()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass