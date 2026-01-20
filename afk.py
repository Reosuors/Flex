import pickle
import asyncio
import json
from datetime import datetime, time as dtime
from telethon import events
from core.client import client

# State
afk_mode = False
custom_reply = "أنا لست موجودًا الآن، أرجوك اترك رسالتك وانتظر لحين عودتي."
reply_to_message = None
custom_replies = {}
custom_replies_enabled = False
allowed_chats = set()
last_reply_sent = None

# Scheduling
SCHEDULE_FILE = "afk_schedule.json"
schedule = {"enabled": False, "start": "22:00", "end": "08:00"}  # default window

def load_schedule():
    global schedule
    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_schedule():
    try:
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(schedule, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

load_schedule()

def within_schedule(now: datetime) -> bool:
    if not schedule.get("enabled"):
        return False
    try:
        start_h, start_m = map(int, schedule["start"].split(":"))
        end_h, end_m = map(int, schedule["end"].split(":"))
        start_t = dtime(start_h, start_m)
        end_t = dtime(end_h, end_m)
    except Exception:
        return False
    # handle overnight windows (e.g., 22:00 -> 08:00)
    if start_t <= end_t:
        return start_t <= now.time() <= end_t
    else:
        return now.time() >= start_t or now.time() <= end_t

# Load stored custom replies if exist
try:
    with open('custom_replies.pickle', 'rb') as f:
        custom_replies = pickle.load(f)
except FileNotFoundError:
    pass


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تشغيل الرد))
async def enable_afk(event):
    global afk_mode
    afk_mode = True
    await event.edit("تم تشغيل الرد التلقائي.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.المخصص تشغيل))
async def enable_custom_replies(event):
    global custom_replies_enabled
    custom_replies_enabled = True
    await event.edit("تم تشغيل الردود المخصصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل الرد))
async def disable_replies(event):
    global afk_mode, custom_replies_enabled
    afk_mode = False
    custom_replies_enabled = False
    await event.edit("تم تعطيل الرد التلقائي والردود المخصصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.كليشة الرد))
async def set_reply_template(event):
    global reply_to_message
    reply_to_message = await event.get_reply_message()
    if reply_to_message:
        await event.edit("تم تعيين كليشة الرد إلى الرسالة المحددة.")
    else:
        await event.edit("يرجى الرد على الرسالة التي تريد استخدامها ككليشة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.رد (.*)'))
async def add_custom_reply(event):
    global custom_replies
    reply_msg = await event.get_reply_message()
    if reply_msg:
        trigger_text = reply_msg.raw_text
        reply_text = event.pattern_match.group(1).strip()
        if len(custom_replies) < 20:
            custom_replies[trigger_text] = reply_text
            with open('custom_replies.pickle', 'wb') as f:
                pickle.dump(custom_replies, f)
            await event.edit(f"تم إضافة الرد المخصص بنجاح. لديك الآن {len(custom_replies)} ردود مخصصة.")
        else:
            await event.edit("لقد وصلت إلى الحد الأقصى للردود المخصصة (20).")
    else:
        await event.edit("يرجى الرد على الرسالة التي تريد إضافة رد مخصص لها.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.حذف رد))
async def delete_custom_reply(event):
    global custom_replies
    reply_msg = await event.get_reply_message()
    if reply_msg:
        trigger_text = reply_msg.raw_text
        if trigger_text in custom_replies:
            del custom_replies[trigger_text]
            with open('custom_replies.pickle', 'wb') as f:
                pickle.dump(custom_replies, f)
            await event.edit("تم حذف الرد المخصص بنجاح.")
        else:
            await event.edit("لم يتم العثور على رد مخصص لهذه الرسالة.")
    else:
        await event.edit("يرجى الرد على الرسالة التي تريد حذف ردها المخصص.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.سماح))
async def allow_chat(event):
    if event.is_private:
        allowed_chats.add(event.chat_id)
        await event.edit("تم السماح لهذه المحادثة.")
    else:
        await event.edit("لا يمكن استخدام هذا الأمر إلا في المحادثات الخاصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.الغاء السماح))
async def disallow_chat(event):
    if event.is_private:
        allowed_chats.discard(event.chat_id)
        await event.edit("تم إلغاء السماح لهذه المحادثة.")
    else:
        await event.edit("لا يمكن استخدام هذا الأمر إلا في المحادثات الخاصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.جدولة_الغياب (\d{2}:\d{2}) (\d{2}:\d{2})))
async def schedule_afk(event):
    start = event.pattern_match.group(1)
    end = event.pattern_match.group(2)
    # basic validation
    try:
        s_h, s_m = map(int, start.split(":"))
        e_h, e_m = map(int, end.split(":"))
        assert 0 <= s_h <= 23 and 0 <= s_m <= 59
        assert 0 <= e_h <= 23 and 0 <= e_m <= 59
    except Exception:
        await event.edit("صيغة الوقت غير صحيحة. استخدم HH:MM HH:MM مثل 22:00 08:00.")
        return
    schedule["enabled"] = True
    schedule["start"] = start
    schedule["end"] = end
    save_schedule()
    await event.edit(f"✓ تم تفعيل جدولة الغياب من {start} إلى {end} يوميًا.")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.الغاء_الجدولة))
async def unschedule_afk(event):
    schedule["enabled"] = False
    save_schedule()
    await event.edit("✓ تم إلغاء جدولة الغياب.")

@client.on(events.NewMessage)
async def reply_handler(event):
    global last_reply_sent, afk_mode
    # Auto-toggle AFK based on schedule
    if schedule.get("enabled"):
        now = datetime.now()
        afk_mode = within_schedule(now)

    if (afk_mode or custom_replies_enabled) and event.is_private and event.chat_id not in allowed_chats:
        me = await event.client.get_me()
        sender = await event.get_sender()
        if sender.id != me.id and not sender.bot:
            if custom_replies_enabled:
                for trigger, reply in custom_replies.items():
                    if trigger and trigger in (event.raw_text or ""):
                        await event.reply(reply)
                        break
            if afk_mode:
                if not (event.raw_text or "") in custom_replies:
                    if reply_to_message and (reply_to_message.text or "").strip():
                        reply_text = reply_to_message.text
                        reply = await event.reply(reply_text)
                        if last_reply_sent and getattr(last_reply_sent, "text", None) == reply_text:
                            try:
                                await last_reply_sent.delete()
                            except Exception:
                                pass
                        last_reply_sent = reply
                    else:
                        reply = await event.reply(custom_reply)
                        if last_reply_sent and getattr(last_reply_sent, "text", None) == custom_reply:
                            try:
                                await last_reply_sent.delete()
                            except Exception:
                                pass
                        last_reply_sent = reply