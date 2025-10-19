import os
from telethon import events
from core.client import client

shortcuts = {}
MEMES_DB = {}


@client.on(events.NewMessage(pattern=r"^\.اختصار \+ (\S+)$"))
async def add_shortcut(event):
    key = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        shortcuts[key] = reply_message.text
        await event.edit(f"**⎙ تم حفظ الاختصار ({key}) ⇨ {reply_message.text}**")
    else:
        await event.edit("**⎙ يجب الرد على رسالة لاختصارها.**")


@client.on(events.NewMessage)
async def get_shortcut(event):
    text = (event.raw_text or "").strip()
    if text in shortcuts and event.out:
        await event.edit(shortcuts[text])


@client.on(events.NewMessage(pattern=r"^\.حذف اختصار \+ (\S+)$"))
async def delete_shortcut(event):
    key = event.pattern_match.group(1)
    if key in shortcuts:
        del shortcuts[key]
        await event.edit(f"**⎙ تم حذف الاختصار ({key})**")
    else:
        await event.edit(f"**⎙ لا يوجد اختصار بهذا الاسم ({key})**")


@client.on(events.NewMessage(pattern=r"^\.الاختصارات$"))
async def list_shortcuts(event):
    if shortcuts:
        text = "\n".join([f"{k} ⇨ {v}" for k, v in shortcuts.items()])
        await event.edit(f"**⎙ قائمة الاختصارات:\n{text}**")
    else:
        await event.edit("**⎙ لا توجد اختصارات محفوظة.**")


@client.on(events.NewMessage(pattern=r"^\.ميمز (\S+) (.+)"))
async def add_meme(event):
    key = event.pattern_match.group(1)
    url = event.pattern_match.group(2)
    MEMES_DB[key] = url
    await event.edit(f"**᯽︙ تم إضافة البصمة '{key}' بنجاح ✓**")


@client.on(events.NewMessage(pattern=r"^٠/()(\\S+)"))
async def get_meme(event):
    # Pattern in original code seems broken; keeping a placeholder no-op
    pass


@client.on(events.NewMessage(pattern=r"^\.قائمة الميمز$"))
async def list_memes(event):
    if MEMES_DB:
        message = "**᯽︙ قائمة تخزين أوامر الميمز:**\n"
        for key in MEMES_DB:
            message += f"- البصمة: `{key}`\n"
    else:
        message = "**᯽︙ لا توجد بصمات ميمز مخزنة حتى الآن**"
    await event.edit(message)


@client.on(events.NewMessage(pattern=r"^ازالة(?:\s|$)([\s\S]*)"))
async def delete_meme(event):
    key = event.pattern_match.group(1).strip()
    if key in MEMES_DB:
        del MEMES_DB[key]
        await event.edit(f"**᯽︙ تم حذف البصمة '{key}' بنجاح ✓**")
    else:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")


@client.on(events.NewMessage(pattern=r"^\.ازالة_البصمات$"))
async def delete_all_memes(event):
    MEMES_DB.clear()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة ✓**")