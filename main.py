import asyncio
from core.logging_config import setup_logging
from app.loader import load_plugins
from app.runner import run as run_client
from core.error_reporting import patch_client_error_reporting

async def main():
    setup_logging()
    try:
        patch_client_error_reporting()
    except Exception:
        pass
    load_plugins()
    await run_client()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up the loop and stop it
        loop.stop()
        # Close the loop if it's still running (e.g., if it was stopped by loop.stop())
        if loop.is_running():
            loop.close()