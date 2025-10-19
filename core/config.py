import os

# Accept multiple common env var names for convenience on different hosts
API_ID_KEYS = ["API_ID", "APP_ID", "TG_API_ID", "TELEGRAM_API_ID"]
API_HASH_KEYS = ["API_HASH", "APP_HASH", "TG_API_HASH", "TELEGRAM_API_HASH"]
SESSION_KEYS = ["STRING_SESSION", "TELETHON_STRING", "SESSION"]

def _read_first(keys):
    for k in keys:
        v = os.environ.get(k)
        if v:
            return k, v
    return None, None

API_ID_KEY, API_ID = _read_first(API_ID_KEYS)
API_HASH_KEY, API_HASH = _read_first(API_HASH_KEYS)
SESSION_KEY, STRING_SESSION = _read_first(SESSION_KEYS)

def _mask(v, keep=4):
    if not v:
        return ""
    if len(v) <= keep*2:
        return "*" * len(v)
    return v[:keep] + "..." + v[-keep:]

if not API_ID or not API_HASH or not STRING_SESSION:
    print("[config] Missing one of API_ID / API_HASH / STRING_SESSION in environment.")
    print(f"[config] Resolved keys: API_ID=({API_ID_KEY} -> {_mask(API_ID)}), "
          f"API_HASH=({API_HASH_KEY} -> {_mask(API_HASH)}), "
          f"STRING_SESSION=({SESSION_KEY} -> {_mask(STRING_SESSION, keep=6)})")