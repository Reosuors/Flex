import asyncio
from core.logging_config import setup_logging

from app.loader import load_plugins
from app.runner import run as run_client
from core.error_reporting import patch_client_error_reporting


async def main():
    setup_logging()

    # Patch error reporting BEFORE loading plugins so all handlers get wrapped
    try:
        patch_client_error_reporting()
    except Exception:
        # If patch fails, continue without breaking startup
        pass

    # Load all plugins (handlers will attach to the shared client)
    load_plugins()

    # Start client and block
    await run_client()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass