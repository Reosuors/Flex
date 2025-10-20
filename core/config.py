import os

# Accept multiple common env var names for convenience on different hosts
API_ID_KEYS = ["API_ID", "APP_ID", "TG_API_ID", "TELEGRAM_API_ID"]
API_HASH_KEYS = ["API_HASH", "APP_HASH", "TG_API_HASH", "TELEGRAM_API_HASH"]
SESSION_KEYS = ["STRING_SESSION", "TELETHON_STRING", "SESSION"]
BOT_TOKEN_KEYS = ["BOT_TOKEN", "TELEGRAM_BOT_TOKEN"]

def _read_first(keys):
    for k in keys:
        v = os.environ.get(k)
        if v:
            return k, v
    return None, None

API_ID_KEY, API_ID = _read_first(API_ID_KEYS)
API_HASH_KEY, API_HASH = _read_first(API_HASH_KEYS)
SESSION_KEY, STRING_SESSION = _read_first(SESSION_KEYS)
BOT_TOKEN_KEY, BOT_TOKEN = _read_first(BOT_TOKEN_KEYS)

def _mask(v, keep=4):
    if not v:
        return ""
    if len(v) <= keep*2:
        return "*" * len(v)
    return v[:keep] + "..." + v[-keep:]

if not API_ID or not API_HASH:
    print("[config] Missing API_ID/API_HASH in environment.")
    print(f"[config] Resolved keys: API_ID=({API_ID_KEY} -> {_mask(API_ID)}), "
          f"API_HASH=({API_HASH_KEY} -> {_mask(API_HASH)})")

if not STRING_SESSION and not BOT_TOKEN:
    print("[config] Missing STRING_SESSION. BOT mode is optional; set BOT_TOKEN to run as bot instead.")
    print(f"[config] Resolved keys: STRING_SESSION=({SESSION_KEY} -> {_mask(STRING_SESSION, keep=6)}), "
          f"BOT_TOKEN=({BOT_TOKEN_KEY} -> {_mask(BOT_TOKEN, keep=6)})")