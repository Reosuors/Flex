import os
from telethon import events
from core.client import client

# Default remote URLs (can be overridden by env vars)
DEFAULT_AR_URL = "https://files.catbox.moe/fcqmhx.jpeg"

def project_file(*parts: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *parts))

def resolve_image(candidates: list[str], env_var: str, default_url: str | None = None) -> str | None:
    """
    Return first existing local image from candidates, or an URL from env var,
    otherwise use provided default_url if any.
    """
    for p in candidates:
        if p and os.path.exists(p):
            return p
    url = os.environ.get(env_var) or default_url
    if url:
        return url
    return None

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    img = resolve_image(
        [project_file("flex_ar.jpg"), project_file("flex.jpg")],
        "FLEX_AR_URL",
        DEFAULT_AR_URL,
    )
    if img:
        await client.send_file(event.chat_id, file=img, caption="سورس فليكس شغال ✅ استمتع")
    else:
        await event.reply("سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    img = resolve_image(
        [project_file("flex_en.jpg")],
        "FLEX_EN_URL",
        None,
    )
    if img:
        await client.send_file(event.chat_id, file=img, caption="Flex source is running ✅ Enjoy")
    else:
        await event.reply("Flex source is running ✅ Enjoy")