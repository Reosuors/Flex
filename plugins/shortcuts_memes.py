import os
import json
from telethon import events
from core.client import client

shortcuts = {}
MEMES_DB = {}
_MEMES_FILE = "memes_db.json"


def _load_memes():
    global MEMES_DB
    if os.path.exists(_MEMES_FILE) and os.stat(_MEMES_FILE).st_size > 0:
        try:
            with open(_MEMES_FILE, "r", encoding="utf-8") as f:
                MEMES_DB = json.load(f)
        except Exception:
            MEMES_DB = {}
    else:
        MEMES_DB = {}


def _save_memes():
    try:
        with open(_MEMES_FILE, "w", encoding="utf-8") as f:
            json.dump(MEMES_DB, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# initialize on import
_load_memes()


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
    _save_memes()
    await event.edit(f"**᯽︙ تم إضافة البصمة '{key}' بنجاح ✓**")


# إصلاح نمط الجلب المكسور وإضافة أمر واضح
@client.on(events.NewMessage(pattern=r"^\.ميمز (جلب|عرض) (\S+)$"))
async def get_meme(event):
    action = event.pattern_match.group(1)
    key = event.pattern_match.group(2)
    url = MEMES_DB.get(key)
    if not url:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")
        return
    # اعرض الرابط أو أرسل الملف بحسب المحتوى
    if url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm", ".webp")):
        await event.delete()
        await client.send_file(event.chat_id, url, caption=f"᯽︙ {key}")
    else:
        await event.edit(f"᯽︙ {key} ⇨ {url}")


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
        _save_memes()
        await event.edit(f"**᯽︙ تم حذف البصمة '{key}' بنجاح ✓**")
    else:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")


@client.on(events.NewMessage(pattern=r"^\.ازالة_البصمات$"))
async def delete_all_memes(event):
    MEMES_DB.clear()
    _save_memes()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة ✓**")