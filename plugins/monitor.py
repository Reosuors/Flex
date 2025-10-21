import os
import pickle
import datetime
from telethon import events, functions
from core.client import client

watchlist_file = "watchlist.pkl"
monitoring_group_file = "monitoring_group.pkl"
user_data_file = "user_data.pkl"
change_log_file = "user_change_log.pkl"

watchlist = {}
user_data = {}
change_log = {}  # {user_id: [(timestamp, change_text), ...]}
monitoring_group = None

def _load_pickle(path, default):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception:
            return default
    return default

watchlist = _load_pickle(watchlist_file, {})
user_data = _load_pickle(user_data_file, {})
change_log = _load_pickle(change_log_file, {})
monitoring_group = _load_pickle(monitoring_group_file, None)

def save_watchlist():
    with open(watchlist_file, "wb") as f:
        pickle.dump(watchlist, f)

def save_user_data():
    with open(user_data_file, "wb") as f:
        pickle.dump(user_data, f)

def save_change_log():
    with open(change_log_file, "wb") as f:
        pickle.dump(change_log, f)

def save_monitoring_group():
    with open(monitoring_group_file, "wb") as f:
        pickle.dump(monitoring_group, f)

async def ensure_monitoring_group():
    global monitoring_group
    if monitoring_group:
        return monitoring_group
    try:
        result = await client(functions.channels.CreateChannelRequest(
            title="📡 مجموعة المراقبة",
            about="قناة خاصة لمراقبة الأشخاص",
            megagroup=True
        ))
        monitoring_group = result.chats[0].id
        save_monitoring_group()
    except Exception:
        monitoring_group = None
    return monitoring_group

@client.on(events.NewMessage(pattern=r"\.مراقبة (.+)"))
async def start_watching(event):
    global monitoring_group
    username = event.pattern_match.group(1)
    monitoring_group = await ensure_monitoring_group()
    if monitoring_group is None:
        await event.reply("⎙ فشل في إنشاء مجموعة المراقبة. حاول لاحقًا.")
        return
    try:
        user = await client.get_entity(username)
        if user.id in watchlist:
            await event.reply(f"⎙ المستخدم @{username} قيد المراقبة بالفعل.")
            return
        watchlist[user.id] = user.username or f"ID_{user.id}"
        user_data[user.id] = {'name': user.first_name, 'photo': None, 'bio': None}
        change_log.setdefault(user.id, [])
        save_watchlist()
        save_user_data()
        save_change_log()
        await event.reply(f"⎙ بدأت مراقبة المستخدم: @{watchlist[user.id]}")
    except Exception:
        await event.reply(f"⎙ لم يتم العثور على المستخدم @{username}.")

@client.on(events.NewMessage(pattern=r"\.ايقاف_المراقبة (.+)"))
async def stop_watching(event):
    username = event.pattern_match.group(1)
    try:
        user = await client.get_entity(username)
        if user.id in watchlist:
            watchlist.pop(user.id, None)
            user_data.pop(user.id, None)
            change_log.pop(user.id, None)
            save_watchlist()
            save_user_data()
            save_change_log()
            await event.reply(f"⎙ تم إيقاف مراقبة المستخدم: @{username}")
        else:
            await event.reply(f"⎙ المستخدم @{username} غير موجود في قائمة المراقبة.")
    except Exception:
        await event.reply(f"⎙ لم يتم العثور على المستخدم @{username}.")

@client.on(events.UserUpdate)
async def user_update_handler(event):
    global monitoring_group
    if not monitoring_group:
        return
    user_id = event.user_id
    if user_id in watchlist:
        try:
            user = await client.get_entity(user_id)
            old = user_data.get(user_id, {})
            changes = []
            if user.first_name != old.get('name'):
                changes.append(f"📌 الاسم الجديد: {user.first_name}")
                user_data[user_id]['name'] = user.first_name
            if user.username and user.username != watchlist[user_id]:
                changes.append(f"🔗 اليوزر الجديد: @{user.username}")
                watchlist[user_id] = user.username
            photos = await client.get_profile_photos(user_id, limit=1)
            if photos:
                new_photo_id = photos[0].id
                if new_photo_id != old.get('photo'):
                    changes.append("🖼️ قام بتغيير صورته الشخصية")
                    user_data[user_id]['photo'] = new_photo_id
            full_user = await client(functions.users.GetFullUserRequest(user))
            if full_user.about and full_user.about != old.get('bio'):
                changes.append(f"📝 قام بتغيير البايو: {full_user.about}")
                user_data[user_id]['bio'] = full_user.about

            save_user_data()
            save_watchlist()
            if changes:
                ts = datetime.datetime.utcnow().isoformat()
                log_entries = change_log.setdefault(user_id, [])
                for ch in changes:
                    log_entries.append((ts, ch))
                save_change_log()
                user_mention = f"@{watchlist[user_id]}" if watchlist[user_id] else f"ID: {user_id}"
                await client.send_message(monitoring_group, f"⎙ تحديث في حساب {user_mention}:\n\n" + "\n".join(changes))
        except Exception:
            pass

@client.on(events.NewMessage(pattern=r"\.تقرير_اسبوعي$"))
async def weekly_report(event):
    monitoring_group_id = await ensure_monitoring_group()
    if not monitoring_group_id:
        await event.edit("⚠️ لم يتم إعداد مجموعة المراقبة.")
        return
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    lines = ["╔══════════════════════════════╗", "║ تقرير تغييرات أسبوعي • FLEX ║", "╚══════════════════════════════╝", ""]
    total_changes = 0
    for uid, entries in change_log.items():
        recent = [f"{ts}: {txt}" for ts, txt in entries if datetime.datetime.fromisoformat(ts) >= cutoff]
        if recent:
            title = watchlist.get(uid) or f"ID_{uid}"
            lines.append(f"• @{title} ({uid}):")
            lines.extend([f"  - {e}" for e in recent])
            lines.append("")
            total_changes += len(recent)
    if total_changes == 0:
        await event.edit("لا توجد تغييرات خلال الأسبوع الماضي.")
        return
    report = "\n".join(lines)
    await event.edit(report)