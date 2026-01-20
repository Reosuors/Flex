import os
import json
from telethon import events
from core.client import client

DATA_FILE = "responses.json"


def _load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"responses": {}, "enabled_groups": [], "priorities": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("responses", {})
            data.setdefault("enabled_groups", [])
            data.setdefault("priorities", {})
            return data
    except Exception as e:
        print(f"[auto_reply] load error: {e}")
        return {"responses": {}, "enabled_groups": [], "priorities": {}}


def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


DATA = _load_data()


@client.on(events.NewMessage(pattern=r"^\.اضف رد \+ (.+) \+ (.+)$"))
@client.on(events.NewMessage(pattern=r"^\.add_reply \+ (.+) \+ (.+)$"))
async def add_response(event):
    try:
        # split by ' + ' keeps compatibility AR/EN
        _, key, value = event.raw_text.split(" + ", 2)
        key = key.strip()
        value = value.strip()
        DATA["responses"][key] = value
        DATA["priorities"].setdefault(key, 1)
        _save_data(DATA)
        await event.edit(f"⎙ تم إضافة الرد بنجاح:\n**{key} → {value}** (الأولوية: {DATA['priorities'][key]})")
    except ValueError:
        await event.edit("⎙ الصيغة غير صحيحة. استخدم: `.اضف رد + الكلمة + الرد` | `.add_reply + KEY + VALUE`")


@client.on(events.NewMessage(pattern=r"^\.أولوية الرد (\S+) (\d+)$"))
@client.on(events.NewMessage(pattern=r"^\.reply_priority (\S+) (\d+)$"))
async def set_priority(event):
    key = event.pattern_match.group(1)
    pr = int(event.pattern_match.group(2))
    if key not in DATA["responses"]:
        await event.edit("⎙ لا يوجد رد بهذه الكلمة.")
        return
    DATA["priorities"][key] = max(1, pr)
    _save_data(DATA)
    await event.edit(f"✓ تم تعيين أولوية الرد للكلمة '{key}' إلى {pr}.")


@client.on(events.NewMessage(pattern=r"^\.الردود$"))
@client.on(events.NewMessage(pattern=r"^\.replies$"))
async def list_responses(event):
    responses = DATA.get("responses", {})
    if responses:
        lines = []
        for k, v in responses.items():
            p = DATA["priorities"].get(k, 1)
            lines.append(f"⎙ **{k}** (أولوية {p}) → {v}")
        msg = "**⎙ الردود المخزنة:**\n\n" + "\n".join(lines)
    else:
        msg = "⎙ لا توجد ردود مخزنة."
    await event.reply(msg)


@client.on(events.NewMessage(pattern=r"^\.تفعيل هنا$"))
@client.on(events.NewMessage(pattern=r"^\.enable_here$"))
async def enable_group(event):
    chat_id = event.chat_id
    if chat_id not in DATA["enabled_groups"]:
        DATA["enabled_groups"].append(chat_id)
        _save_data(DATA)
    await event.edit("**⎙ تم تفعيل الردود التلقائية في هذه المجموعة.**")


@client.on(events.NewMessage(pattern=r"^\.تعطيل هنا$"))
@client.on(events.NewMessage(pattern=r"^\.disable_here$"))
async def disable_group(event):
    chat_id = event.chat_id
    if chat_id in DATA["enabled_groups"]:
        DATA["enabled_groups"].remove(chat_id)
        _save_data(DATA)
        await event.edit("**⎙ تم تعطيل الردود التلقائية في هذه المجموعة.**")
    else:
        await event.edit("**⎙ الردود التلقائية غير مفعلة هنا.**")


@client.on(events.NewMessage)
async def auto_reply(event):
    # ignore own outgoing to avoid loops
    if event.out:
        return
    if event.chat_id in DATA.get("enabled_groups", []):
        text = (event.raw_text or "").strip()
        if not text:
            return
        # pick best match by priority supporting substring triggers
        matches = []
        for k, v in DATA["responses"].items():
            if k == text or (k in text and len(k) >= 2):
                pr = DATA["priorities"].get(k, 1)
                matches.append((pr, len(k), v))
        if not matches:
            return
        # highest priority, then longest key
        matches.sort(key=lambda x: (x[0], x[1]), reverse=True)
        value = matches[0][2]
        # do not reply to bots to reduce noise
        try:
            sender = await event.get_sender()
            if getattr(sender, "bot", False):
                return
        except Exception:
            pass
        await event.reply(value)