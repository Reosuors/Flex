import os

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # optional, for assistant bot with inline buttons
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or "gsk_HSKVk5cU6ED3m955YvWGdyb3FYUjyYZUEwzNwfAS4GIGMeZgvX"
DATABASE_URL = os.environ.get("DATABASE_URL")  # optional, used when available

def _validate() -> int:
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not STRING_SESSION:
        missing.append("STRING_SESSION")

    if missing:
        # Fail fast to avoid cryptic errors when creating the client
        print(f"[config] Missing required environment variables: {', '.join(missing)}")
        raise SystemExit(1)

    try:
        return int(API_ID)
    except (TypeError, ValueError):
        print("[config] API_ID must be a valid integer.")
        raise SystemExit(1)

# Parsed and validated API_ID as int
API_ID_INT = _validate()
