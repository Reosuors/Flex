import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logging.getLogger("telethon").setLevel(logging.WARNING)