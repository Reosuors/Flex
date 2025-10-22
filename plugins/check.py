from telethon import events
from core.client import client

# Simple health-check command: ".فحص"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source(event):
    # Reply that the source is working
    await event.reply("سورس فليكس شغال ✅ استمتع")