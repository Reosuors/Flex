from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.users import GetFullUserRequest
from core.client import client
import json
import os
from datetime import datetime

ACTIONS_FILE = "admin_actions.json"

def _load_actions():
    if os.path.exists(ACTIONS_FILE) and os.stat(ACTIONS_FILE).st_size > 0:
        try:
            with open(ACTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_actions(actions):
    try:
        with open(ACTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(actions, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

admin_actions = _load_actions()

async def resolve_target(event):
    getmessage = await event.get_reply_message()
    if getmessage:
        return getmessage.sender_id
    try:
        return int(event.text.split(" ", 1)[1])
    except Exception:
        if event.message.entities:
            for entity in event.message.entities:
                if hasattr(entity, 'user_id'):
                    return entity.user_id
        return None

def log_action(action, target_id, chat_id, reason=""):
    admin_actions.append({
        "ts": datetime.utcnow().isoformat(),
        "action": action,
        "target_id": target_id,
        "chat_id": getattr(chat_id, "channel_id", getattr(chat_id, "chat_id", chat_id)),
        "reason": reason
    })
    _save_actions(admin_actions)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.(حظر|طرد|تقييد)(?:\s+(.+))?))
async def runkick(event):
    await event.edit("جارٍ...")
    await event.delete()
    command = event.pattern_match.group(1)
    reason = (event.pattern_match.group(2) or "").strip()
    targetuser = await resolve_target(event)
    if not targetuser:
        await event.respond("يرجى الرد على المستخدم لاتمام الامر")
        return
    try:
        targetdetails = await client(GetFullUserRequest(targetuser))
        messagelocation = event.to_id
        if command == "طرد":
            await event.client.kick_participant(messagelocation, targetuser)
            action = "⎉╎ تم حظر"
        elif command == "حظر":
            await client(EditBannedRequest(messagelocation, targetuser, ChatBannedRights(until_date=None, view_messages=True)))
            action = "⎉╎ تم حظره"
        elif command == "تقييد":
            await client(EditBannedRequest(messagelocation, targetuser, ChatBannedRights(until_date=None, send_messages=True)))
            action = "⎉╎ تم تقييده"
        await event.client.send_message(messagelocation, f"<a href='tg://user?id={targetuser}'>{targetdetails.users[0].first_name}</a> {action}", parse_mode="html")
        log_action(command, targetuser, messagelocation, reason)
    except Exception as e:
        await event.respond(f"حدث خطأ: {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.(الغاء الحظر|الغاء التقييد)(?:\s+(.+))?))
async def unrunkick(event):
    await event.edit("جارٍ...")
    await event.delete()
    command = event.pattern_match.group(1)
    reason = (event.pattern_match.group(2) or "").strip()
    targetuser = await resolve_target(event)
    if not targetuser:
        await event.respond(". يرجى الرد على المستخدم")
        return
    try:
        targetdetails = await client(GetFullUserRequest(targetuser))
        messagelocation = event.to_id
        await client(EditBannedRequest(messagelocation, targetuser, ChatBannedRights(until_date=None, view_messages=False, send_messages=False)))
        action = "⎉╎ تم إلغاء حظره" if command == "الغاء الحظر" else "⎉╎ تم إلغاء تقييده"
        await event.client.send_message(messagelocation, f"<a href='tg://user?id={targetuser}'>{targetdetails.users[0].first_name}</a> {action}", parse_mode="html")
        log_action(command, targetuser, messagelocation, reason)
    except Exception as e:
        await event.respond(f"حدث خطأ: {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.سجل_إداري))
async def show_admin_log(event):
    if not admin_actions:
        await event.edit("لا يوجد سجل إداري حتى الآن.")
        return
    lines = ["╔══════════════════════╗", "║ سجل إداري • FLEX     ║", "╚══════════════════════╝", ""]
    for a in admin_actions[-25:]:  # show last 25 actions
        lines.append(f"- {a['ts']} | {a['action']} | target={a['target_id']} | chat={a['chat_id']}" + (f" | سبب: {a['reason']}" if a.get("reason") else ""))
    await event.edit("\n".join(lines))