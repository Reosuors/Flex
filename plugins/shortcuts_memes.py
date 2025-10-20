import os
import json
from telethon import events
from core.client import client

shortcuts = {}
MEMES_DB = {}
_MEMES_FILE = "memes_db.json"
_SHORTCUTS_FILE = "shortcuts.json"
_MEMES_DIR = "memes"


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


def _load_shortcuts():
    global shortcuts
    if os.path.exists(_SHORTCUTS_FILE) and os.stat(_SHORTCUTS_FILE).st_size > 0:
        try:
            with open(_SHORTCUTS_FILE, "r", encoding="utf-8") as f:
                shortcuts = json.load(f)
        except Exception:
            shortcuts = {}
    else:
        shortcuts = {}


def _save_shortcuts():
    try:
        with open(_SHORTCUTS_FILE, "w", encoding="utf-8") as f:
            json.dump(shortcuts, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _ensure_memes_dir():
    try:
        os.makedirs(_MEMES_DIR, exist_ok=True)
    except Exception:
        pass


# initialize on import
_load_memes()
_load_shortcuts()
_ensure_memes_dir()


@client.on(events.NewMessage(pattern=r"^\.اختصار \+ (\S+)$"))
async def add_shortcut(event):
    key = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        shortcuts[key] = reply_message.text
        _save_shortcuts()
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
        _save_shortcuts()
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
    # إضافة بواسطة مفتاح + رابط
    key = event.pattern_match.group(1)
    url = event.pattern_match.group(2)
    MEMES_DB[key] = url
    _save_memes()
    await event.edit(f"**᯽︙ تم إضافة البصمة '{key}' بنجاح ✓**")


@client.on(events.NewMessage(pattern=r"^\.ميمز حفظ (\S+)$"))
async def add_meme_from_reply(event):
    # إضافة بواسطة الرد على وسائط
    key = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        await event.edit("**⎙ يجب الرد على صورة/فيديو لحفظها كبصمة.**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("**⎙ الرسالة لا تحتوي على وسائط.**")
        return
    try:
        _ensure_memes_dir()
        # سمّي الملف بشكل قابل للتفريق
        file_path = os.path.join(_MEMES_DIR, f"{key}_{reply_message.id}")
        saved = await reply_message.download_media(file=file_path)
        # Telethon قد يضيف الامتداد تلقائيًا، نستخدم المسار المرجع النهائي
        MEMES_DB[key] = saved
        _save_memes()
        await event.edit(f"**᯽︙ تم حفظ البصمة '{key}' من الوسائط ✓**")
    except Exception as e:
        await event.edit(f"**❌ فشل حفظ الوسائط: {e}**")


# إصلاح نمط الجلب وإضافة أمر واضح
@client.on(events.NewMessage(pattern=r"^\.ميمز (جلب|عرض) (\S+)$"))
async def get_meme(event):
    action = event.pattern_match.group(1)
    key = event.pattern_match.group(2)
    url = MEMES_DB.get(key)
    if not url:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")
        return
    # إذا كان رابط/مسار لوسائط — أرسل كملف
    lower = url.lower()
    if lower.endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm", ".webp")) or os.path.exists(url):
        await event.delete()
        try:
            await client.send_file(event.chat_id, url, caption=f"᯽︙ {key}")
        except Exception as e:
            await client.send_message(event.chat_id, f"**❌ فشل إرسال الملف:** {e}")
    else:
        await event.edit(f"᯽︙ {key} ⇨ {url}")


@client.on(events.NewMessage(pattern=r"^\.قائمة الميمز$"))
async def list_memes(event):
    if MEMES_DB:
        message = "**᯽︙ قائمة تخزين أوامر الميمز:**\n"
        for key, value in MEMES_DB.items():
            kind = "ملف" if os.path.exists(value) else "رابط"
            message += f"- البصمة: `{key}` ({kind})\n"
    else:
        message = "**᯽︙ لا توجد بصمات ميمز مخزنة حتى الآن**"
    await event.edit(message)


@client.on(events.NewMessage(pattern=r"^ازالة(?:\s|$)([\s\S]*)"))
async def delete_meme(event):
    key = event.pattern_match.group(1).strip()
    if key in MEMES_DB:
        val = MEMES_DB[key]
        # إن كان ملفًا محليًا احذفه أيضًا
        if os.path.exists(val):
            try:
                os.remove(val)
            except Exception:
                pass
        del MEMES_DB[key]
        _save_memes()
        await event.edit(f"**᯽︙ تم حذف البصمة '{key}' بنجاح ✓**")
    else:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")


@client.on(events.NewMessage(pattern=r"^\.ازالة_البصمات$"))
async def delete_all_memes(event):
    # حذف جميع الملفات المحلية إن وجدت
    for key, val in list(MEMES_DB.items()):
        if os.path.exists(val):
            try:
                os.remove(val)
            except Exception:
                pass
    MEMES_DB.clear()
    _save_memes()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة ✓**")