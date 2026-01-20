from telethon import events
from core.client import client

@client.on(events.NewMessage(outgoing=True, pattern=r"\.السورس$"))
async def source_ar_command(event):
    message = (
        "⋆─┄─┄─┄─  S O U R C E  F L Ξ X  ─┄─┄─┄─⋆\n\n"
        "𓆩 ⚡ ꜱᴏᴜʀᴄᴇ » SOURCE FLEX\n"
        "𓆩 🔗 ʟɪɴᴋ   » https://t.me/sourceflex\n\n"
        "⋆───⋆ [ ⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ  S O U R C E  F L Ξ X ™ ] ⋆───⋆\n\n"
        "المطور: @FO_5O"
    )
    await event.edit(message)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.source$"))
async def source_en_command(event):
    message = (
        "⋆─┄─┄─┄─  S O U R C E  F L Ξ X  ─┄─┄─┄─⋆\n\n"
        "𓆩 ⚡ ꜱᴏᴜʀᴄᴇ » SOURCE FLEX\n"
        "𓆩 🔗 ʟɪɴᴋ   » https://t.me/sourceflex\n\n"
        "⋆───⋆ [ ⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ  S O U R C E  F L Ξ X ™ ] ⋆───⋆\n\n"
        "Developer: @FO_5O"
    )
    await event.edit(message)
