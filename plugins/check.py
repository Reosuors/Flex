import os
from telethon import events
from core.client import client

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    # Send the bundled image with Arabic caption
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    img_path = os.path.join(project_root, "flex.jpg")
    await client.send_file(event.chat_id, file=img_path, caption="سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    await event.reply("Flex source is running ✅ Enjoy")