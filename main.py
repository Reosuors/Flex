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
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود. تأكد من تعيينه في متغيرات البيئة")
    
bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = "data.json"

# تحميل وحفظ البيانات
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

user_data = load_data()

# ======== نظام الترجمة المتعددة اللغات ========
def setup_localization():
    """إعداد نظام الترجمة"""
    translations = {
        "ar": {
            "welcome": "مرحباً! 🌍",
            "start_message": "أهلاً بك في بوت النشر التلقائي",
            "help": "🆘 المساعدة",
            "cancel": "إلغاء",
            "send_api_id": "أرسل **API ID** أولاً أو اضغط 'إلغاء'.",
            "send_api_hash": "تمام ✅ الآن أرسل **API HASH**:",
            "send_session": "تمام ✅ الآن أرسل **String Session**:",
            "session_saved": "✔️ السيشن محفوظ. الآن ارسل الرسالة يلي بدك تنشرها:",
            "send_count": "كم مرة بدك تنشرها؟",
            "send_delay": "قديش الفاصل الزمني بين كل رسالة (ثواني)؟",
            "setup_complete": "✅ كل البيانات جاهزة! اضغط /menu للتحكم الكامل",
            "press_menu": "اضغط /menu لتفتح الخيارات",
            "operation_cancelled": "❌ تم إلغاء العملية. ابدا من جديد /start",
            "input_error": "✖️ خطأ بالمدخل، جرب ترسل البيانات مرة ثانية.",
            "not_started": "❌ لم تبدأ العملية، اضغط /start",
            "choose_action": "اختر العملية:",
            "set_new_msg": "اكتب الرسالة الجديدة أو 'إلغاء'",
            "set_new_count": "اكتب العدد الجديد أو 'إلغاء'",
            "set_new_delay": "اكتب الفاصل الجديد بالثواني أو 'إلغاء'",
            "no_groups_selected": "❌ ما في قروبات مختارة",
            "choose_group_to_remove": "اختر القروب لحذفه:",
            "group_removed": "❌ حذفت {}",
            "group_added": "✔️ أضفت {}",
            "choose_groups": "اختر القروبات:",
            "connection_failed": "❌ فشل الاتصال: {}",
            "incomplete_data": "❌ البيانات غير مكتملة",
            "no_groups_chosen": "❌ لم تختر أي قروبات",
            "sending_complete": "✔️ تم إرسال {} رسالة بنجاح.",
            "error_occurred": "✖️ خطأ: {}",
            "current_settings": "📋 الإعدادات الحالية:",
            "security_advice": "💡 نصيحة الأمان:",
            "reset_complete": "🚫 تم حذف كل البيانات. ابدا من جديد /start"
        },
        "en": {
            "welcome": "Welcome! 🌍",
            "start_message": "Welcome to Auto Post Bot",
            "help": "🆘 Help",
            "cancel": "Cancel",
            "send_api_id": "Send **API ID** first or press 'Cancel'.",
            "send_api_hash": "OK ✅ Now send **API HASH**:",
            "send_session": "OK ✅ Now send **String Session**:",
            "session_saved": "✔️ Session saved. Now send the message you want to publish:",
            "send_count": "How many times do you want to send it?",
            "send_delay": "What is the time interval between each message (seconds)?",
            "setup_complete": "✅ All data is ready! Press /menu for full control",
            "press_menu": "Press /menu to open options",
            "operation_cancelled": "❌ Operation cancelled. Start again with /start",
            "input_error": "✖️ Input error, try sending the data again.",
            "not_started": "❌ You haven't started, press /start",
            "choose_action": "Choose action:",
            "set_new_msg": "Write the new message or 'Cancel'",
            "set_new_count": "Write the new count or 'Cancel'",
            "set_new_delay": "Write the new delay in seconds or 'Cancel'",
            "no_groups_selected": "❌ No groups selected",
            "choose_group_to_remove": "Choose group to remove:",
            "group_removed": "❌ Removed {}",
            "group_added": "✔️ Added {}",
            "choose_groups": "Choose groups:",
            "connection_failed": "❌ Connection failed: {}",
            "incomplete_data": "❌ Incomplete data",
            "no_groups_chosen": "❌ No groups chosen",
            "sending_complete": "✔️ Successfully sent {} messages.",
            "error_occurred": "✖️ Error: {}",
            "current_settings": "📋 Current settings:",
            "security_advice": "💡 Security advice:",
            "reset_complete": "🚫 All data deleted. Start again with /start"
        }
    }
    return translations

def get_message(uid, key, **format_args):
    """الحصول على رسالة مترجمة"""
    lang = user_data.get(uid, {}).get("language", "ar")
    translations = setup_localization()
    message = translations.get(lang, {}).get(key, translations["ar"].get(key, key))
    
    # تطبيق التنسيق إذا كان هناك معاملات
    if format_args:
        try:
            message = message.format(**format_args)
        except:
            pass
            
    return message

# ======== START ========
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user_data[uid] = {"waiting": "api_id", "language": "ar"}
    save_data()
    bot.send_message(message.chat.id, get_message(uid, "welcome"))
    bot.send_message(message.chat.id, get_message(uid, "send_api_id"))

# ======== استقبال النصوص ========
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    uid = str(message.chat.id)
    if uid not in user_data:
        bot.send_message(message.chat.id, get_message(uid, "press_menu"))
        return
        
    data = user_data.get(uid, {})
    task = data.get("waiting")

    if not task:
        bot.send_message(message.chat.id, get_message(uid, "press_menu"))
        return

    cancel_text = get_message(uid, "cancel")
    if message.text.lower() == cancel_text.lower():
        user_data.pop(uid, None)
        save_data()
        bot.send_message(message.chat.id, get_message(uid, "operation_cancelled"))
        return

    try:
        if task == "api_id":
            user_data[uid]["api_id"] = int(message.text)
            user_data[uid]["waiting"] = "api_hash"
            bot.send_message(message.chat.id, get_message(uid, "send_api_hash"))
        elif task == "api_hash":
            user_data[uid]["api_hash"] = message.text
            user_data[uid]["waiting"] = "session"
            bot.send_message(message.chat.id, get_message(uid, "send_session"))
        elif task == "session":
            user_data[uid]["session"] = message.text
            user_data[uid]["waiting"] = "msg"
            bot.send_message(message.chat.id, get_message(uid, "session_saved"))
        elif task == "msg":
            user_data[uid]["message"] = message.text
            user_data[uid]["waiting"] = "count"
            bot.send_message(message.chat.id, get_message(uid, "send_count"))
        elif task == "count":
            user_data[uid]["count"] = int(message.text)
            user_data[uid]["waiting"] = "delay"
            bot.send_message(message.chat.id, get_message(uid, "send_delay"))
        elif task == "delay":
            user_data[uid]["delay"] = int(message.text)
            user_data[uid]["waiting"] = None
            bot.send_message(message.chat.id, get_message(uid, "setup_complete"))
        save_data()
    except ValueError:
        bot.send_message(message.chat.id, get_message(uid, "input_error"))
    except Exception as e:
        bot.send_message(message.chat.id, get_message(uid, "error_occurred", error=str(e)))

# ======== MENU ========
@bot.message_handler(commands=['menu'])
def menu(message):
    uid = str(message.chat.id)
    if uid not in user_data:
        bot.send_message(message.chat.id, get_message(uid, "not_started"))
        return
        
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 " + get_message(uid, "set_new_msg").split(' أو ')[0], callback_data="set_msg"))
    markup.add(InlineKeyboardButton("🔢 " + get_message(uid, "set_new_count").split(' أو ')[0], callback_data="set_count"))
    markup.add(InlineKeyboardButton("⏱️ " + get_message(uid, "set_new_delay").split(' أو ')[0], callback_data="set_delay"))
    markup.add(InlineKeyboardButton("📂 " + get_message(uid, "choose_groups"), callback_data="choose_groups"))
    markup.add(InlineKeyboardButton("❌ " + get_message(uid, "choose_group_to_remove"), callback_data="remove_group"))
    markup.add(InlineKeyboardButton("ℹ️ " + get_message(uid, "current_settings"), callback_data="show_settings"))
    markup.add(InlineKeyboardButton("💡 " + get_message(uid, "security_advice"), callback_data="advice"))
    markup.add(InlineKeyboardButton("🚀 ابدأ النشر", callback_data="start_send"))
    markup.add(InlineKeyboardButton("🚫 " + get_message(uid, "reset_complete").split('.')[0], callback_data="reset"))
    
    # زر تغيير اللغة
    current_lang = user_data[uid].get("language", "ar")
    lang_button = "🌐 English" if current_lang == "ar" else "🌐 العربية"
    markup.add(InlineKeyboardButton(lang_button, callback_data="toggle_language"))
    
    bot.send_message(message.chat.id, get_message(uid, "choose_action"), reply_markup=markup)

# ======== أزرار CALLBACK ========
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = str(call.message.chat.id)
    if uid not in user_data:
        bot.send_message(call.message.chat.id, get_message(uid, "not_started"))
        return

    if call.data == "set_msg":
        user_data[uid]["waiting"] = "msg"
        bot.send_message(call.message.chat.id, get_message(uid, "set_new_msg"))
    elif call.data == "set_count":
        user_data[uid]["waiting"] = "count"
        bot.send_message(call.message.chat.id, get_message(uid, "set_new_count"))
    elif call.data == "set_delay":
        user_data[uid]["waiting"] = "delay"
        bot.send_message(call.message.chat.id, get_message(uid, "set_new_delay"))
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
        bot.send_message(call.message.chat.id, get_message(uid, "reset_complete"))
    elif call.data == "toggle_language":
        # تبديل اللغة
        current_lang = user_data[uid].get("language", "ar")
        new_lang = "en" if current_lang == "ar" else "ar"
        user_data[uid]["language"] = new_lang
        save_data()
        bot.send_message(call.message.chat.id, f"🌐 Language changed to {new_lang}")
        menu(call.message)  # إعادة عرض القائمة باللغة الجديدة
    save_data()

# ======== عرض الإعدادات ========
def show_settings(uid, chat_id):
    data = user_data.get(uid, {})
    selected_groups = data.get('selected', [])
    groups_list = '\n'.join([g.get('title', 'بدون عنوان') for g in selected_groups]) if selected_groups else get_message(uid, "no_groups_selected")
    
    text = f"""
{get_message(uid, "current_settings")}
API ID: {data.get('api_id', '❌')}
API HASH: {data.get('api_hash', '❌')}
Session: {'✔️ ' + get_message(uid, "session_saved").split('.')[0] if 'session' in data else '❌'}
📝 {get_message(uid, "set_new_msg").split(' أو ')[0]}: {data.get('message','❌')}
🔢 {get_message(uid, "set_new_count").split(' أو ')[0]}: {data.get('count','❌')}
⏱️ {get_message(uid, "set_new_delay").split(' أو ')[0]}: {data.get('delay','❌')} {get_message(uid, "send_delay").split('(')[1].split(')')[0]}
📂 {get_message(uid, "choose_groups")}: 
{groups_list}
"""
    bot.send_message(chat_id, text)

# ======== نصائح الأمان ========
def show_advice(chat_id):
    uid = str(chat_id)
    advice = f"""
{get_message(uid, "security_advice")}
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
        bot.send_message(chat_id, get_message(uid, "no_groups_selected"))
        return
    markup = InlineKeyboardMarkup(row_width=1)
    for i, g in enumerate(selected):
        markup.add(InlineKeyboardButton(f"❌ {g.get('title', 'بدون عنوان')}", callback_data=f"delg_{i}"))
    bot.send_message(chat_id, get_message(uid, "choose_group_to_remove"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delg_"))
def delete_group(call):
    uid = str(call.message.chat.id)
    if uid not in user_data:
        bot.answer_callback_query(call.id, get_message(uid, "not_started"))
        return
        
    idx = int(call.data.split("_")[1])
    if "selected" in user_data[uid] and idx < len(user_data[uid]["selected"]):
        removed = user_data[uid]["selected"].pop(idx)
        save_data()
        bot.answer_callback_query(call.id, get_message(uid, "group_removed", group_name=removed.get('title', 'المجموعة')))
    else:
        bot.answer_callback_query(call.id, get_message(uid, "error_occurred", error="لم أتمكن من إزالة المجموعة"))

# ======== Telethon اختيار القروبات ========
def fetch_groups(uid, chat_id):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_fetch_groups(uid, chat_id))
    except Exception as e:
        bot.send_message(chat_id, get_message(uid, "error_occurred", error=str(e)))

async def _fetch_groups(uid, chat_id):
    data = user_data.get(uid, {})
    if not all(key in data for key in ["session", "api_id", "api_hash"]):
        bot.send_message(chat_id, get_message(uid, "incomplete_data"))
        return
        
    try:
        client = TelegramClient(StringSession(data["session"]), data["api_id"], data["api_hash"])
        await client.start()
        dialogs = await client.get_dialogs()
        groups = [d for d in dialogs if isinstance(d.entity, (Channel, Chat)) and d.is_group]

        user_data[uid]["groups"] = [{"id": g.entity.id, "title": g.entity.title} for g in groups]
        save_data()

        markup = InlineKeyboardMarkup(row_width=1)
        for i, g in enumerate(groups):
            markup.add(InlineKeyboardButton(g.entity.title, callback_data=f"g_{i}"))
        bot.send_message(chat_id, get_message(uid, "choose_groups"), reply_markup=markup)
        await client.disconnect()
    except Exception as e:
        bot.send_message(chat_id, get_message(uid, "connection_failed", error=str(e)))

@bot.callback_query_handler(func=lambda call: call.data.startswith("g_"))
def choose_group(call):
    uid = str(call.message.chat.id)
    if uid not in user_data:
        bot.answer_callback_query(call.id, get_message(uid, "not_started"))
        return
        
    try:
        idx = int(call.data.split("_")[1])
        if "groups" not in user_data[uid] or idx >= len(user_data[uid]["groups"]):
            bot.answer_callback_query(call.id, get_message(uid, "error_occurred", error="المجموعة غير موجودة"))
            return
            
        g = user_data[uid]["groups"][idx]
        if "selected" not in user_data[uid]:
            user_data[uid]["selected"] = []
        user_data[uid]["selected"].append(g)
        save_data()
        bot.answer_callback_query(call.id, get_message(uid, "group_added", group_name=g.get('title', 'المجموعة')))
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, get_message(uid, "error_occurred", error="خطأ في اختيار المجموعة"))

# ======== بدء النشر ========
def start_sending(uid, chat_id):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_start_sending(uid, chat_id))
    except Exception as e:
        bot.send_message(chat_id, get_message(uid, "error_occurred", error=str(e)))

async def _start_sending(uid, chat_id):
    try:
        data = user_data.get(uid, {})
        if not all(key in data for key in ["session", "api_id", "api_hash", "message", "count", "delay"]):
            bot.send_message(chat_id, get_message(uid, "incomplete_data"))
            return
            
        groups = data.get("selected", [])
        if not groups:
            bot.send_message(chat_id, get_message(uid, "no_groups_chosen"))
            return

        client = TelegramClient(StringSession(data["session"]), data["api_id"], data["api_hash"])
        await client.start()
        msg = data["message"]
        count = data["count"]
        delay = data["delay"]

        total_sent = 0
        for g in groups:
            for i in range(count):
                try:
                    await client.send_message(g["id"], msg)
                    total_sent += 1
                    time.sleep(delay)
                except Exception as e:
                    print(f"خطأ في إرسال الرسالة: {e}")
        await client.disconnect()
        bot.send_message(chat_id, get_message(uid, "sending_complete", count=total_sent))
    except Exception as e:
        bot.send_message(chat_id, get_message(uid, "error_occurred", error=str(e)))

# ======== تشغيل ========
if __name__ == "__main__":
    print("Bot is running ...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ فشل تشغيل البوت: {str(e)}")
