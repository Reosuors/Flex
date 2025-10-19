import os

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")

if not API_ID or not API_HASH or not STRING_SESSION:
    # Keep it lightweight: just warn. Validation can be expanded later.
    print("[config] Missing one of API_ID / API_HASH / STRING_SESSION in environment.")