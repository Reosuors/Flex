import os

# Accept multiple common env var names for convenience on different hosts
API_ID = (
    os.environ.get("API_ID")
    or os.environ.get("APP_ID")
    or os.environ.get("TG_API_ID")
    or os.environ.get("TELEGRAM_API_ID")
)
API_HASH = (
    os.environ.get("API_HASH")
    or os.environ.get("APP_HASH")
    or os.environ.get("TG_API_HASH")
    or os.environ.get("TELEGRAM_API_HASH")
)
STRING_SESSION = os.environ.get("STRING_SESSION") or os.environ.get("TELETHON_STRING") or os.environ.get("SESSION")

if not API_ID or not API_HASH or not STRING_SESSION:
    # Keep it lightweight: just warn. Validation can be expanded later.
    print("[config] Missing one of API_ID / API_HASH / STRING_SESSION in environment. "
          "Tried keys: API_ID/APP_ID/TG_API_ID/TELEGRAM_API_ID and API_HASH/APP_HASH/TG_API_HASH/TELEGRAM_API_HASH.")