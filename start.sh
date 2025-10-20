#!/usr/bin/env bash
set -e

echo "[start] Python version: $(python3 --version)"
echo "[start] Working dir: $(pwd)"
echo "[start] Listing repo files:"
ls -la

echo "[start] Dumping relevant env keys (masked):"
mask() { python3 - <<'PY'
import os, sys
def m(v, k=4):
    if not v: return ""
    return (v[:k] + "..." + v[-k:]) if len(v) > k*2 else "*"*len(v)
keys = [
    ("API_ID", os.getenv("API_ID")),
    ("APP_ID", os.getenv("APP_ID")),
    ("TG_API_ID", os.getenv("TG_API_ID")),
    ("TELEGRAM_API_ID", os.getenv("TELEGRAM_API_ID")),
    ("API_HASH", os.getenv("API_HASH")),
    ("APP_HASH", os.getenv("APP_HASH")),
    ("TG_API_HASH", os.getenv("TG_API_HASH")),
    ("TELEGRAM_API_HASH", os.getenv("TELEGRAM_API_HASH")),
    ("STRING_SESSION", os.getenv("STRING_SESSION")),
    ("TELETHON_STRING", os.getenv("TELETHON_STRING")),
    ("SESSION", os.getenv("SESSION")),
]
for k, v in keys:
    if v:
        print(f"{k}={m(v,6)}")
PY
}
mask

export PYTHONUNBUFFERED=1

echo "[start] Launching health server and client..."
python3 yeman_server.py &

# Small delay to ensure health server binds to the port
sleep 1

python3 main.py