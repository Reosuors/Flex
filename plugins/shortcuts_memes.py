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

def _ensure_entry(key):
    entry = MEMES_DB.get(key)
    if isinstance(entry, str):
        # migrate to structured format
        MEMES_DB[key] = {"src": entry, "tags": []}
    elif entry is None:
        MEMES_DB[key] = {"src": "", "tags": []}
    return MEMES_DB[key]

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
    entry = _ensure_entry(key)
    entry["src"] = url
    MEMES_DB[key] = entry
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
        entry = _ensure_entry(key)
        entry["src"] = saved
        MEMES_DB[key] = entry
        _save_memes()
        await event.edit(f"**᯽︙ تم حفظ البصمة '{key}' من الوسائط ✓**")
    except Exception as e:
        await event.edit(f"**❌ فشل حفظ الوسائط: {e}**")

# وسم الميمز
@client.on(events.NewMessage(pattern=r"^\.وسم_ميمز (\S+)(?:\s+(.+))?$"))
async def tag_meme(event):
    key = event.pattern_match.group(1)
    tags_raw = (event.pattern_match.group(2) or "").strip()
    if key not in MEMES_DB:
        await event.edit("لا توجد بصمة بهذا الاسم.")
        return
    tags = [t.strip("# ").lower() for t in tags_raw.split() if t.strip()]
    entry = _ensure_entry(key)
    for t in tags:
        if t and t not in entry["tags"]:
            entry["tags"].append(t)
    MEMES_DB[key] = entry
    _save_memes()
    await event.edit(f"✓ تم تحديث وسوم '{key}': {', '.join(entry['tags']) or 'بدون'}")

@client.on(events.NewMessage(pattern=r"^\.بحث_ميمز (\S+)$"))
async def search_memes(event):
    tag = event.pattern_match.group(1).strip("# ").lower()
    results = []
    for k, entry in MEMES_DB.items():
        entry = _ensure_entry(k)
        if tag in entry.get("tags", []):
            results.append(k)
    if not results:
        await event.edit("لا نتائج للوسم المطلوب.")
    else:
        await event.edit("نتائج البحث:\n- " + "\n- ".join(results))

# إصلاح نمط الجلب وإضافة أمر واضح
@client.on(events.NewMessage(pattern=r"^\.ميمز (جلب|عرض) (\S+)$"))
async def get_meme(event):
    action = event.pattern_match.group(1)
    key = event.pattern_match.group(2)
    entry = MEMES_DB.get(key)
    if not entry:
        await event.edit(f"**❌ لم يتم العثور على بصمة بهذا الاسم '{key}'**")
        return
    if isinstance(entry, str):
        src = entry
    else:
        src = entry.get("src") or ""
    # إذا كان رابط/مسار لوسائط — أرسل كملف
    lower = src.lower()
    if lower.endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4", ".webm", ".webp")) or os.path.exists(src):
        await event.delete()
        try:
            await client.send_file(event.chat_id, src, caption=f"᯽︙ {key}")
        except Exception as e:
            await client.send_message(event.chat_id, f"**❌ فشل إرسال الملف:** {e}")
    else:
        await event.edit(f"᯽︙ {key} ⇨ {src}")

@client.on(events.NewMessage(pattern=r"^\.قائمة الميمز$"))
async def list_memes(event):
    if MEMES_DB:
        message = "**᯽︙ قائمة تخزين أوامر الميمز:**\n"
        for key, value in MEMES_DB.items():
            entry = _ensure_entry(key)
            kind = "ملف" if os.path.exists(entry.get("src", "")) else "رابط"
            tags = entry.get("tags", [])
            message += f"- `{key}` ({kind}) — وسوم: {', '.join(tags) or 'بدون'}\n"
    else:
        message = "**᯽︙ لا توجد بصمات ميمز مخزنة حتى الآن**"
    await event.edit(message)

@client.on(events.NewMessage(pattern=r"^ازالة(?:\s|$)([\s\S]*)"))
async def delete_meme(event):
    key = event.pattern_match.group(1).strip()
    if key in MEMES_DB:
        val = MEMES_DB[key]
        src = val if isinstance(val, str) else val.get("src", "")
        # إن كان ملفًا محليًا احذفه أيضًا
        if os.path.exists(src):
            try:
                os.remove(src)
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
        src = val if isinstance(val, str) else val.get("src", "")
        if os.path.exists(src):
            try:
                os.remove(src)
            except Exception:
                pass
    MEMES_DB.clear()
    _save_memes()
    await event.edit("**᯽︙ تم حذف جميع بصمات الميمز من القائمة ✓**")