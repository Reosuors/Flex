from telethon import events
from core.client import client

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    await event.reply("سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    await event.reply("Flex source is running ✅ Enjoy")