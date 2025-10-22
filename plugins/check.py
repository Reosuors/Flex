import os
from telethon import events
from core.client import client

def project_file(*parts: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *parts))

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    # Prefer flex_ar.jpg; fallback to existing flex.jpg
    img_ar_path = project_file("flex_ar.jpg")
    img_fallback = project_file("flex.jpg")
    if os.path.exists(img_ar_path):
        await client.send_file(event.chat_id, file=img_ar_path, caption="سورس فليكس شغال ✅ استمتع")
    elif os.path.exists(img_fallback):
        await client.send_file(event.chat_id, file=img_fallback, caption="سورس فليكس شغال ✅ استمتع")
    else:
        await event.reply("سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    # Prefer flex_en.jpg; fallback to text
    img_en_path = project_file("flex_en.jpg")
    if os.path.exists(img_en_path):
        await client.send_file(event.chat_id, file=img_en_path, caption="Flex source is running ✅ Enjoy")
    else:
        await event.reply("Flex source is running ✅ Enjoy")