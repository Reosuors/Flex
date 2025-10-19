import pickle
import asyncio
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

# Load stored custom replies if exist
try:
    with open('custom_replies.pickle', 'rb') as f:
        custom_replies = pickle.load(f)
except FileNotFoundError:
    pass


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تشغيل الرد$'))
async def enable_afk(event):
    global afk_mode
    afk_mode = True
    await event.edit("تم تشغيل الرد التلقائي.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.المخصص تشغيل$'))
async def enable_custom_replies(event):
    global custom_replies_enabled
    custom_replies_enabled = True
    await event.edit("تم تشغيل الردود المخصصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل الرد$'))
async def disable_replies(event):
    global afk_mode, custom_replies_enabled
    afk_mode = False
    custom_replies_enabled = False
    await event.edit("تم تعطيل الرد التلقائي والردود المخصصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.كليشة الرد$'))
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


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.حذف رد$'))
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


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.سماح$'))
async def allow_chat(event):
    if event.is_private:
        allowed_chats.add(event.chat_id)
        await event.edit("تم السماح لهذه المحادثة.")
    else:
        await event.edit("لا يمكن استخدام هذا الأمر إلا في المحادثات الخاصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.الغاء السماح$'))
async def disallow_chat(event):
    if event.is_private:
        allowed_chats.discard(event.chat_id)
        await event.edit("تم إلغاء السماح لهذه المحادثة.")
    else:
        await event.edit("لا يمكن استخدام هذا الأمر إلا في المحادثات الخاصة.")
    await asyncio.sleep(2)
    await event.delete()


@client.on(events.NewMessage)
async def reply_handler(event):
    global last_reply_sent
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
                    if reply_to_message:
                        reply_text = reply_to_message.text
                        reply = await event.reply(reply_to_message)
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