import os
import pickle
import datetime
from telethon import events
from core.client import client

STATE_FILE = "member_add_limit.pkl"
LIMIT_PER_DAY = 1  # الحد الافتراضي للاضافة يوميًا لكل شخص
WHITELIST = set()  # يمكن لاحقًا إضافة معرفات يتم استثناؤهم

# الحالة: {adder_id: {"date": "YYYY-MM-DD", "count": int}}
state = {}

def load_state():
    global state
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "rb") as f:
                state = pickle.load(f)
        except Exception:
            state = {}
    else:
        state = {}

def save_state():
    try:
        with open(STATE_FILE, "wb") as f:
            pickle.dump(state, f)
    except Exception:
        pass

load_state()

def today_str():
    return datetime.date.today().isoformat()

def can_add_today(adder_id: int) -> bool:
    if adder_id in WHITELIST:
        return True
    rec = state.get(adder_id)
    if not rec:
        return True
    if rec.get("date") != today_str():
        return True
    return rec.get("count", 0) < LIMIT_PER_DAY

def register_add(adder_id: int):
    rec = state.get(adder_id)
    if not rec or rec.get("date") != today_str():
        state[adder_id] = {"date": today_str(), "count": 1}
    else:
        state[adder_id]["count"] = state[adder_id].get("count", 0) + 1
    save_state()

@client.on(events.ChatAction())
async def on_member_added(event):
    # فقط في المجموعات والقنوات الخارقة
    if not (event.is_group or event.is_channel):
        return
    # نحتاج لحالة إضافة عضو جديد
    if not (getattr(event, "user_added", False) or (getattr(event, "users", None) or [])):
        return

    adder_id = event.sender_id  # الشخص الذي قام بالإضافة
    added_users = getattr(event, "users", []) or ([getattr(event, "user_id", None)] if getattr(event, "user_id", None) else [])
    if not added_users:
        return

    # تحقق الحد
    if can_add_today(adder_id):
        register_add(adder_id)
        return

    # تجاوز الحد: احذف الرسالة (إن أمكن) وألغِ إضافة المستخدمين (طردهم)
    # ملاحظة: قد يفشل الطرد إن لم تكن لديك صلاحيات
    try:
        await event.delete()
    except Exception:
        pass

    # حاول طرد كل من تمت إضافتهم
    kicked = []
    for uid in added_users:
        try:
            if uid is not None:
                await client.kick_participant(event.chat_id, uid)
                kicked.append(uid)
        except Exception:
            # قد لا نملك صلاحيات أو العضو لا يمكن طرده
            pass

    # رسالة تحذير للمضيف
    try:
        me = await client.get_me()
        if adder_id != me.id:
            mention = f"<a href='tg://user?id={adder_id}'>المضيف</a>"
        else:
            mention = "المضيف"
        msg = (
            f"⚠️ {mention}: لقد تجاوزت حد إضافة الأعضاء المسموح به ({LIMIT_PER_DAY}) لهذا اليوم.\n"
        )
        if kicked:
            msg += f"تم إلغاء إضافة ({len(kicked)}) عضو{'ًا' if len(kicked)==1 else ''}."
        await client.send_message(event.chat_id, msg, parse_mode="html")
    except Exception:
        pass

# أوامر ضبط بسيطة (اختيارية):

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعيين حد الاضافة (\d+)$"))
async def set_limit(event):
    global LIMIT_PER_DAY
    try:
        LIMIT_PER_DAY = int(event.pattern_match.group(1))
        await event.edit(f"✓ تم تعيين حد الإضافة اليومي إلى: {LIMIT_PER_DAY}")
    except Exception:
        await event.edit("تعذر تعيين الحد. تأكد من الصيغة: .تعيين حد الاضافة <رقم>")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.مسح سجل الاضافة$"))
async def clear_limit_state(event):
    global state
    state = {}
    save_state()
    await event.edit("✓ تم مسح سجل الإضافات اليومي لجميع المستخدمين.")