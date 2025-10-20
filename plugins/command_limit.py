import os
import pickle
import datetime
from telethon import events
from core.client import client

STATE_FILE = "command_usage_limit.pkl"

# Structure:
# state = {
#   "limits": {"cmd_name": int},            # per-command daily limit (default 1)
#   "enabled": set(["cmd_name", ...]),      # commands with limit enforcement
#   "usage": {                              
#       "user_id": {
#           "cmd_name": {"date": "YYYY-MM-DD", "count": int}
#       }
#   }
# }
state = {
    "limits": {},
    "enabled": set(),
    "usage": {}
}

def load_state():
    global state
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "rb") as f:
                state = pickle.load(f)
            # Convert enabled to set if loaded as list
            if not isinstance(state.get("enabled"), set):
                state["enabled"] = set(state.get("enabled", []))
        except Exception:
            pass

def save_state():
    try:
        # Serialize set as list
        to_save = dict(state)
        to_save["enabled"] = list(state["enabled"])
        with open(STATE_FILE, "wb") as f:
            pickle.dump(to_save, f)
    except Exception:
        pass

def today_str():
    return datetime.date.today().isoformat()

def get_limit(cmd: str) -> int:
    return int(state["limits"].get(cmd, 1))

def can_use(user_id: int, cmd: str) -> bool:
    usage = state["usage"].get(user_id, {}).get(cmd)
    if not usage:
        return True
    if usage.get("date") != today_str():
        return True
    return usage.get("count", 0) < get_limit(cmd)

def register_use(user_id: int, cmd: str):
    user_usage = state["usage"].setdefault(user_id, {})
    rec = user_usage.get(cmd)
    if not rec or rec.get("date") != today_str():
        user_usage[cmd] = {"date": today_str(), "count": 1}
    else:
        user_usage[cmd]["count"] = user_usage[cmd].get("count", 0) + 1
    save_state()

load_state()

def parse_command(text: str) -> str:
    text = (text or "").strip()
    if not text.startswith("."):
        return ""
    # command name is token after '.'
    first = text.split(None, 1)[0]
    return first[1:]  # remove leading dot

@client.on(events.NewMessage(outgoing=True))
async def enforce_command_limit(event):
    cmd = parse_command(event.raw_text or "")
    if not cmd or cmd not in state["enabled"]:
        return
    me = await client.get_me()
    user_id = me.id
    if can_use(user_id, cmd):
        register_use(user_id, cmd)
        return
    # Limit exceeded: prevent execution
    try:
        await event.delete()
    except Exception:
        pass
    try:
        await client.send_message(
            event.chat_id,
            f"⚠️ لقد استخدمت الأمر .{cmd} الحدّ المسموح به لهذا اليوم.\nيمكنك إعادة المحاولة غدًا.",
        )
    except Exception:
        pass

# Management commands
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تفعيل حد الامر (\S+)$"))
async def enable_cmd_limit(event):
    cmd = event.pattern_match.group(1)
    state["enabled"].add(cmd)
    save_state()
    await event.edit(f"✓ تم تفعيل حد الاستخدام اليومي للأمر: .{cmd} (الافتراضي مرة واحدة يوميًا).")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعطيل حد الامر (\S+)$"))
async def disable_cmd_limit(event):
    cmd = event.pattern_match.group(1)
    state["enabled"].discard(cmd)
    save_state()
    await event.edit(f"✓ تم تعطيل حد الاستخدام اليومي للأمر: .{cmd}.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تعيين حد الامر (\S+) (\d+)$"))
async def set_cmd_limit(event):
    cmd = event.pattern_match.group(1)
    limit = int(event.pattern_match.group(2))
    if limit <= 0:
        await event.edit("الحد يجب أن يكون رقمًا موجبًا.")
        return
    state["limits"][cmd] = limit
    save_state()
    await event.edit(f"✓ تم تعيين حد الاستخدام اليومي للأمر .{cmd} إلى: {limit}.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.مسح سجل الامر (\S+)$"))
async def clear_cmd_usage(event):
    cmd = event.pattern_match.group(1)
    for uid, cmds in list(state["usage"].items()):
        if cmd in cmds:
            del cmds[cmd]
    save_state()
    await event.edit(f"✓ تم مسح سجل الاستخدام اليومي للأمر .{cmd} لجميع المستخدمين.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.حالة حد الامر (\S+)$"))
async def status_cmd_limit(event):
    cmd = event.pattern_match.group(1)
    enabled = cmd in state["enabled"]
    limit = get_limit(cmd)
    await event.edit(
        f"حالة حد الأمر .{cmd}:\n"
        f"- مفعل؟ {'نعم' if enabled else 'لا'}\n"
        f"- الحد اليومي: {limit}\n"
    )