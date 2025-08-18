# -*- coding: utf-8 -*-
# بوت نشر تلقائي كامل + أزرار تحكم كامل + نصائح أمان
# pyTelegramBotAPI + Telethon + JSON + InlineKeyboardButtons

import os
import telebot
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat
import asyncio
import threading
import time
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن يقرأ من Environment Variable على Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = "data.json"

# تحميل وحفظ البيانات
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

user_data = load_data()

# ======== START ========
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user_data[uid] = {}
    save_data()
    bot.send_message(message.chat.id, "هلا! ✌️ رح نبدأ إعداد البوت خطوة خطوة.\nأرسل **API ID** أولاً أو اضغط 'إلغاء'.")
    user_data[uid]["waiting"] = "api_id"

# ======== استقبال النصوص ========
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = str(message.chat.id)
    data = user_data.get(uid, {})
    task = data.get("waiting")

    if not task:
        bot.send_message(message.chat.id, "اضغط /menu لتفتح الخيارات")
        return

    if message.text.lower() == "إلغاء":
        user_data.pop(uid, None)
        save_data()
        bot.send_message(message.chat.id, "❌ تم إلغاء العملية. ابدا من جديد /start")
        return

    try:
        if task == "api_id":
            user_data[uid]["api_id"] = int(message.text)
            user_data[uid]["waiting"] = "api_hash"
            bot.send_message(message.chat.id, "تمام ✅ الآن أرسل **API HASH**:")
        elif task == "api_hash":
            user_data[uid]["api_hash"] = message.text
            user_data[uid]["waiting"] = "session"
            bot.send_message(message.chat.id, "تمام ✅ الآن أرسل **String Session**:")
        elif task == "session":
            user_data[uid]["session"] = message.text
            user_data[uid]["waiting"] = "msg"
            bot.send_message(message.chat.id, "✔️ السيشن محفوظ. الآن ارسل الرسالة يلي بدك تنشرها:")
        elif task == "msg":
            user_data[uid]["message"] = message.text
            user_data[uid]["waiting"] = "count"
            bot.send_message(message.chat.id, "كم مرة بدك تنشرها؟")
        elif task == "count":
            user_data[uid]["count"] = int(message.text)
            user_data[uid]["waiting"] = "delay"
            bot.send_message(message.chat.id, "قديش الفاصل الزمني بين كل رسالة (ثواني)؟")
        elif task == "delay":
            user_data[uid]["delay"] = int(message.text)
            user_data[uid]["waiting"] = None
            bot.send_message(message.chat.id, "✅ كل البيانات جاهزة! اضغط /menu للتحكم الكامل")
        save_data()
    except:
        bot.send_message(message.chat.id, "✖️ خطأ بالمدخل، جرب ترسل البيانات مرة ثانية.")

# ======== MENU ========
@bot.message_handler(commands=['menu'])
def menu(message):
    uid = str(message.chat.id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 تغيير الرسالة", callback_data="set_msg"))
    markup.add(InlineKeyboardButton("🔢 تغيير عدد المرات", callback_data="set_count"))
    markup.add(InlineKeyboardButton("⏱️ تغيير الفاصل", callback_data="set_delay"))
    markup.add(InlineKeyboardButton("📂 اختيار القروبات", callback_data="choose_groups"))
    markup.add(InlineKeyboardButton("❌ إزالة قروب من المختارة", callback_data="remove_group"))
    markup.add(InlineKeyboardButton("ℹ️ عرض الإعدادات الحالية", callback_data="show_settings"))
    markup.add(InlineKeyboardButton("💡 نصيحة الأمان", callback_data="advice"))
    markup.add(InlineKeyboardButton("🚀 ابدأ النشر", callback_data="start_send"))
    markup.add(InlineKeyboardButton("🚫 حذف الجلسة وإعادة ضبط", callback_data="reset"))
    bot.send_message(message.chat.id, "اختر العملية:", reply_markup=markup)

# ======== أزرار CALLBACK ========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = str(call.message.chat.id)
    if uid not in user_data:
        bot.send_message(call.message.chat.id, "❌ لم تبدأ العملية، اضغط /start")
        return

    if call.data == "set_msg":
        user_data[uid]["waiting"] = "msg"
        bot.send_message(call.message.chat.id, "اكتب الرسالة الجديدة أو 'إلغاء'")
    elif call.data == "set_count":
        user_data[uid]["waiting"] = "count"
        bot.send_message(call.message.chat.id, "اكتب العدد الجديد أو 'إلغاء'")
    elif call.data == "set_delay":
        user_data[uid]["waiting"] = "delay"
        bot.send_message(call.message.chat.id, "اكتب الفاصل الجديد بالثواني أو 'إلغاء'")
    elif call.data == "choose_groups":
        threading.Thread(target=fetch_groups, args=(uid, call.message.chat.id)).start()
    elif call.data == "remove_group":
        remove_group(uid, call.message.chat.id)
    elif call.data == "show_settings":
        show_settings(uid, call.message.chat.id)
    elif call.data == "advice":
        show_advice(call.message.chat.id)
    elif call.data == "start_send":
        threading.Thread(target=start_sending, args=(uid, call.message.chat.id)).start()
    elif call.data == "reset":
        user_data.pop(uid, None)
        save_data()
        bot.send_message(call.message.chat.id, "🚫 تم حذف كل البيانات. ابدا من جديد /start")
    save_data()

# ======== عرض الإعدادات ========
def show_settings(uid, chat_id):
    data = user_data.get(uid, {})
    text = f"""
📋 الإعدادات الحالية:
API ID: {data.get('api_id', '❌')}
API HASH: {data.get('api_hash', '❌')}
Session: {'✔️ محفوظ' if 'session' in data else '❌'}
📝 الرسالة: {data.get('message','❌')}
🔢 العدد: {data.get('count','❌')}
⏱️ الفاصل: {data.get('delay','❌')} ثانية
📂 القروبات المختارة: 
{'\n'.join([g['title'] for g in data.get('selected', [])]) if 'selected' in data else '❌ ما اخترت'}
"""
    bot.send_message(chat_id, text)

# ======== نصائح الأمان ========
def show_advice(chat_id):
    advice = """
💡 نصيحة الأمان:
1- لا ترسل رسائل كثيرة بسرعة عالية، استخدم فاصل زمني مناسب.
2- لا ترسل نفس الرسالة لجميع القروبات بنفس الوقت.
3- لا تستخدم البوت على قروبات كثيرة دفعة واحدة.
4- حاول تنويع الرسائل لو لازم تنشرها بكثرة.
5- لا تزعج أعضاء القروبات، حتى تحمي حسابك.
"""
    bot.send_message(chat_id, advice)

# ======== إزالة قروب ========
def remove_group(uid, chat_id):
    data = user_data.get(uid, {})
    selected = data.get("selected", [])
    if not selected:
        bot.send_message(chat_id, "❌ ما في قروبات مختارة")
        return
    markup = InlineKeyboardMarkup(row_width=1)
    for i, g in enumerate(selected):
        markup.add(InlineKeyboardButton(f"❌ {g['title']}", callback_data=f"delg_{i}"))
    bot.send_message(chat_id, "اختر القروب لحذفه:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delg_"))
def delete_group(call):
    uid = str(call.message.chat.id)
    idx = int(call.data.split("_")[1])
    if "selected" in user_data[uid]:
        removed = user_data[uid]["selected"].pop(idx)
        save_data()
        bot.answer_callback_query(call.id, f"❌ حذفت {removed['title']}")

# ======== Telethon اختيار القروبات ========
def fetch_groups(uid, chat_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_fetch_groups(uid, chat_id))

async def _fetch_groups(uid, chat_id):
    data = user_data[uid]
    client = TelegramClient(StringSession(data["session"]), data["api_id"], data["api_hash"])
    await client.start()
    dialogs = await client.get_dialogs()
    groups = [d for d in dialogs if isinstance(d.entity, (Channel, Chat)) and d.is_group]

    user_data[uid]["groups"] = [{"id": g.id, "title": g.title} for g in groups]
    save_data()

    markup = InlineKeyboardMarkup(row_width=1)
    for i, g in enumerate(groups):
        markup.add(InlineKeyboardButton(g.title, callback_data=f"g_{i}"))
    bot.send_message(chat_id, "اختر القروبات:", reply_markup=markup)
    await client.disconnect()

@bot.callback_query_handler(func=lambda call: call.data.startswith("g_"))
def choose_group(call):
    uid = str(call.message.chat.id)
    idx = int(call.data.split("_")[1])
    g = user_data[uid]["groups"][idx]
    if "selected" not in user_data[uid]:
        user_data[uid]["selected"] = []
    user_data[uid]["selected"].append(g)
    save_data()
    bot.answer_callback_query(call.id, f"✔️ أضفت {g['title']}")

# ======== بدء النشر ========
def start_sending(uid, chat_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_start_sending(uid, chat_id))

async def _start_sending(uid, chat_id):
    try:
        data = user_data[uid]
        client = TelegramClient(StringSession(data["session"]), data["api_id"], data["api_hash"])
        await client.start()
        msg = data["message"]
        count = data["count"]
        delay = data["delay"]
        groups = data.get("selected", [])

        for g in groups:
            for i in range(count):
                try:
                    await client.send_message(g["id"], msg)
                    time.sleep(delay)
                except Exception as e:
                    print("خطأ:", e)
        await client.disconnect()
        bot.send_message(chat_id, "✔️ خلص النشر بكل القروبات المحددة.")
    except Exception as e:
        bot.send_message(chat_id, f"✖️ خطأ: {e}")

# ======== تشغيل ========
print("Bot is running ...")
bot.infinity_polling()
