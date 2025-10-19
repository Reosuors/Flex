from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.users import GetFullUserRequest
from core.client import client


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


@client.on(events.NewMessage(outgoing=True, pattern=r'\.(حظر|طرد|تقييد)'))
async def runkick(event):
    await event.edit("جارٍ...")
    await event.delete()
    command = event.pattern_match.group(1)
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
    except Exception as e:
        await event.respond(f"حدث خطأ: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=r'\.(الغاء الحظر|الغاء التقييد)'))
async def unrunkick(event):
    await event.edit("جارٍ...")
    await event.delete()
    command = event.pattern_match.group(1)
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
    except Exception as e:
        await event.respond(f"حدث خطأ: {e}")