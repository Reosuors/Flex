import os
import json
from telethon import events
from core.client import client

DATA_FILE = "responses.json"


def _load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"responses": {}, "enabled_groups": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "responses" not in data:
                data["responses"] = {}
            if "enabled_groups" not in data:
                data["enabled_groups"] = []
            return data
    except Exception as e:
        print(f"[auto_reply] load error: {e}")
        return {"responses": {}, "enabled_groups": []}


def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


DATA = _load_data()


@client.on(events.NewMessage(pattern=r"\.اضف رد \+ (.+) \+ (.+)"))
async def add_response(event):
    try:
        _, key, value = event.raw_text.split(" + ", 2)
        key = key.strip()
        value = value.strip()
        DATA["responses"][key] = value
        _save_data(DATA)
        await event.edit(f"⎙ تم إضافة الرد بنجاح:\n**{key} → {value}**")
    except ValueError:
        await event.edit("⎙ الصيغة غير صحيحة. استخدم: `.اضف رد + الكلمة + الرد`")


@client.on(events.NewMessage(pattern=r"\.الردود"))
async def list_responses(event):
    responses = DATA.get("responses", {})
    if responses:
        msg = "**⎙ الردود المخزنة:**\n\n" + "\n".join([f"⎙ **{k}** → {v}" for k, v in responses.items()])
    else:
        msg = "⎙ لا توجد ردود مخزنة."
    await event.reply(msg)


@client.on(events.NewMessage(pattern=r"\.تفعيل هنا"))
async def enable_group(event):
    chat_id = event.chat_id
    if chat_id not in DATA["enabled_groups"]:
        DATA["enabled_groups"].append(chat_id)
        _save_data(DATA)
    await event.edit("**⎙ تم تفعيل الردود التلقائية في هذه المجموعة.**")


@client.on(events.NewMessage(pattern=r"\.تعطيل هنا"))
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
    if event.chat_id in DATA.get("enabled_groups", []):
        text = event.raw_text.strip()
        value = DATA["responses"].get(text)
        if value:
            await event.reply(value)