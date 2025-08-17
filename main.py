import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os
import json

# متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = telebot.TeleBot(TOKEN)

# ملفات البيانات
DATA_FILE = 'users.json'
STATUS_FILE = 'bot_status.json'
COMM_FILE = 'communication.json'
LAST_LINK_FILE = 'last_link.json'

# ====== حالة البوت ======
def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {"active": True}

def save_status(status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f)

bot_status = load_status()

# ====== حالة التواصل ======
def load_comm():
    if os.path.exists(COMM_FILE):
        with open(COMM_FILE, 'r') as f:
            return json.load(f)
    return {"enabled": False}

def save_comm(comm):
    with open(COMM_FILE, 'w') as f:
        json.dump(comm, f)

comm_status = load_comm()

# ====== المستخدمون ======
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

# ====== آخر رابط لكل مستخدم ======
def load_last_links():
    if os.path.exists(LAST_LINK_FILE):
        with open(LAST_LINK_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_last_links(links):
    with open(LAST_LINK_FILE, 'w') as f:
        json.dump(links, f)

last_links = load_last_links()

# ====== تحميل الفيديو ======
def download_video(url, filename='video', quality='best'):
    ydl_opts = {
        'outtmpl': f'{filename}.%(ext)s',
        'format': quality,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    return file_path

# ====== /start ======
@bot.message_handler(commands=['start'])
def start(message):
    global bot_status
    users = load_users()
    user_id = str(message.from_user.id)

    # سجل المستخدم الجديد
    if user_id not in users:
        users[user_id] = {"username": message.from_user.username}
        save_users(users)
        bot.send_message(OWNER_ID, f"👤 @{message.from_user.username} فعّل البوت لأول مرة!")

    # تحقق حالة البوت
    if not bot_status.get("active", True) and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ البوت متوقف حالياً من قبل المطور")
        return

    # واجهة المطور
    if message.from_user.id == OWNER_ID:
        markup = InlineKeyboardMarkup()
        # زر تشغيل/إيقاف البوت
        if bot_status.get("active", True):
            markup.add(InlineKeyboardButton("إيقاف البوت ❌", callback_data="stop_bot"))
        else:
            markup.add(InlineKeyboardButton("تشغيل البوت ✅", callback_data="start_bot"))
        # زر تفعيل/إيقاف التواصل
        if comm_status.get("enabled", False):
            markup.add(InlineKeyboardButton("إيقاف التواصل ❌", callback_data="disable_comm"))
        else:
            markup.add(InlineKeyboardButton("تفعيل التواصل ✅", callback_data="enable_comm"))
        # زر تحميل آخر رابط
        markup.add(InlineKeyboardButton("تحميل آخر رابط 🔄", callback_data="last_link"))
        # زر تقرير المستخدمين
        markup.add(InlineKeyboardButton("تقرير المستخدمين 📊", callback_data="report_users"))
        bot.reply_to(message, "🔥 اهلا يا مالك البوت! استخدم القائمة:", reply_markup=markup)
    else:
        bot.reply_to(message, "🔥 ابعت رابط الفيديو لتحميله 🎥")

# ====== استقبال الرسائل ======
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    global bot_status, comm_status, last_links

    user_id = str(message.from_user.id)

    # تحقق حالة البوت
    if user_id != str(OWNER_ID) and not bot_status.get("active", True):
        bot.reply_to(message, "❌ البوت متوقف حالياً من قبل المطور")
        return

    # التواصل مع المالك مفعل
    if user_id != str(OWNER_ID) and comm_status.get("enabled", False):
        bot.send_message(OWNER_ID, f"💬 رسالة من @{message.from_user.username} ({user_id}):\n{message.text}")
        bot.reply_to(message, "✅ رسالتك وصلت للمالك")
        return

    # المالك يرسل رابط فيديو
    if user_id == str(OWNER_ID):
        url = message.text.strip()
        last_links['owner'] = url
        save_last_links(last_links)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تحميل تيك توك", callback_data=f"tiktok|{url}"))
        markup.add(InlineKeyboardButton("تحميل انستغرام", callback_data=f"instagram|{url}"))
        markup.add(InlineKeyboardButton("تحميل بنترست", callback_data=f"pinterest|{url}"))
        markup.add(InlineKeyboardButton("تحميل أي رابط عام", callback_data=f"any|{url}"))
        bot.reply_to(message, "اختر نوع التحميل:", reply_markup=markup)

# ====== التعامل مع الأزرار ======
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global bot_status, comm_status, last_links

    # قائمة المطور
    if call.from_user.id == OWNER_ID:
        if call.data == "stop_bot":
            bot_status["active"] = False
            save_status(bot_status)
            bot.edit_message_text("❌ تم إيقاف البوت حالياً", call.message.chat.id, call.message.message_id)
            return
        elif call.data == "start_bot":
            bot_status["active"] = True
            save_status(bot_status)
            bot.edit_message_text("✅ تم تشغيل البوت", call.message.chat.id, call.message.message_id)
            return
        elif call.data == "enable_comm":
            comm_status["enabled"] = True
            save_comm(comm_status)
            bot.edit_message_text("✅ تم تفعيل التواصل", call.message.chat.id, call.message.message_id)
            return
        elif call.data == "disable_comm":
            comm_status["enabled"] = False
            save_comm(comm_status)
            bot.edit_message_text("❌ تم إيقاف التواصل", call.message.chat.id, call.message.message_id)
            return
        elif call.data == "last_link":
            url = last_links.get('owner')
            if url:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("تحميل تيك توك", callback_data=f"tiktok|{url}"))
                markup.add(InlineKeyboardButton("تحميل انستغرام", callback_data=f"instagram|{url}"))
                markup.add(InlineKeyboardButton("تحميل بنترست", callback_data=f"pinterest|{url}"))
                markup.add(InlineKeyboardButton("تحميل أي رابط عام", callback_data=f"any|{url}"))
                bot.send_message(call.message.chat.id, "اختر نوع التحميل لآخر رابط:", reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, "❌ لا يوجد رابط محفوظ")
            return
        elif call.data == "report_users":
            users = load_users()
            text = f"📊 عدد المستخدمين: {len(users)}\n"
            for uid, info in users.items():
                text += f"- @{info.get('username','')} ({uid})\n"
            bot.send_message(call.message.chat.id, text)
            return

    # التحقق من المالك للبقية
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ هذا البوت حصري للمالك فقط", show_alert=True)
        return

    # تحميل الفيديو
    try:
        platform, url = call.data.split("|")
        bot.edit_message_text("⏳ جاري تحميل الفيديو...", call.message.chat.id, call.message.message_id)

        if platform == "tiktok":
            file_path = download_video(url, 'tiktok')
        elif platform == "instagram":
            file_path = download_video(url, 'insta')
        elif platform == "pinterest":
            file_path = download_video(url, 'pinterest')
        else:
            file_path = download_video(url, 'video')

        with open(file_path, 'rb') as vid:
            bot.send_video(call.message.chat.id, vid)
        os.remove(file_path)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ صار خطأ: {e}")

print("✅ البوت شغال وجاهز مع كل التحسينات")
bot.infinity_polling()