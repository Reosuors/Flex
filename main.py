import asyncio
import os
import threading
from core.logging_config import setup_logging
from app.loader import load_plugins
from app.runner import run as run_client
from core.error_reporting import patch_client_error_reporting
from yeman_server import app as flask_app

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

async def main():
    setup_logging()
    
    # Start Flask in a background thread to keep Render happy
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
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
        if not loop.is_closed():
            loop.close()
