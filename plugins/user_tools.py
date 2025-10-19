import time
import base64
from math import sqrt
from telethon import events, functions, types
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import Channel, Chat, User, MessageActionChannelMigrateFrom
from core.client import client

STAT_INDICATION = "⎙︙ جـاري جـلب الاحصـائيـات إنتظـر ..."
CHANNELS_STR = "⎙︙ قائمة القنوات:\n\n"
CHANNELS_ADMINSTR = "⎙︙ القنوات التي انت مشرف بها:\n\n"
CHANNELS_OWNERSTR = "⎙︙ قنواتك (مالك):\n\n"
GROUPS_STR = "⎙︙ قائمة المجموعات:\n\n"
GROUPS_ADMINSTR = "⎙︙ مجموعات أنت مشرف فيها:\n\n"
GROUPS_OWNERSTR = "⎙︙ مجموعات أنت مالكها:\n\n"


async def edit_or_reply(event, text, buttons=None):
    buttons = buttons or []
    if event.edit_date is None:
        return await event.reply(text, buttons=buttons)
    else:
        return await event.edit(text, buttons=buttons)


@client.on(events.NewMessage(pattern=r"\.قائمه (جميع القنوات|القنوات المشرف عليها |قنواتي)"))
async def list_channels(event):
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    hi, hica, hico = [], [], []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            channel_name = entity.title
            channel_id = entity.id
            is_owner = entity.creator
            is_admin = entity.admin_rights
            if entity.username:
                if entity.megagroup:
                    channel_link = f"{channel_name} ({entity.username})"
                else:
                    channel_link = f"[{channel_name}](https://t.me/{entity.username})"
            else:
                if entity.megagroup:
                    channel_link = f"{channel_name}"
                else:
                    channel_link = f"[{channel_name}](https://t.me/c/{channel_id}/1)"
            if is_owner:
                hico.append(channel_link)
            if is_admin:
                hica.append(channel_link)
            if not is_owner and not is_admin:
                hi.append(channel_link)
    if catcmd == "جميع القنوات":
        output = CHANNELS_STR + "\n".join(f"{k}• {c}" for k, c in enumerate(hi, start=1))
    elif catcmd == "القنوات المشرف عليها":
        output = CHANNELS_ADMINSTR + "\n".join(f"{k}• {c}" for k, c in enumerate(hica, start=1))
    elif catcmd == "قنواتي":
        output = CHANNELS_OWNERSTR + "\n".join(f"{k}• {c}" for k, c in enumerate(hico, start=1))
    stop_time = time.time() - start_time
    output += f"\n\nاستغرق حساب القنوات: {stop_time:.02f} ثانية"
    await catevent.edit(output)


@client.on(events.NewMessage(pattern=r"\.قائمه (جميع المجموعات|مجموعات اديرها|كروباتي)$"))
async def list_groups(event):
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    hi, higa, higo = [], [], []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel) and entity.megagroup
            or not isinstance(entity, Channel) and not isinstance(entity, User) and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if catcmd == "جميع المجموعات":
        output = GROUPS_STR + "\n".join(f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)" for k, i in enumerate(hi, start=1))
    elif catcmd == "مجموعات اديرها":
        output = GROUPS_ADMINSTR + "\n".join(f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)" for k, i in enumerate(higa, start=1))
    elif catcmd == "كروباتي":
        output = GROUPS_OWNERSTR + "\n".join(f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)" for k, i in enumerate(higo, start=1))
    stop_time = time.time() - start_time
    output += f"\nاستغرق حساب المجموعات: {stop_time:.02f} ثانية"
    await catevent.edit(output)


@client.on(events.NewMessage(pattern=r"\.كشف المجموعة(?: |$)(.*)", outgoing=True))
async def info_group(event):
    await event.edit("`جارٍ الفحص ...`")
    chat = event.pattern_match.group(1)
    chat_info = None

    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass

    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id

    try:
        chat_info = await event.client(functions.messages.GetFullChatRequest(chat))
    except Exception:
        try:
            chat_info = await event.client(functions.channels.GetFullChannelRequest(chat))
        except Exception:
            await event.edit("`حدث خطأ في القناة أو المجموعة..`")
            return

    chat_obj_info = await event.client.get_entity(chat_info.chats[0].id)
    broadcast = getattr(chat_obj_info, "broadcast", False)
    chat_type = "قناة" if broadcast else "مجموعة"
    chat_title = chat_obj_info.title

    try:
        msg_info = await event.client(GetHistoryRequest(
            peer=chat_obj_info.id, offset_id=0, offset_date=None,
            add_offset=-1, limit=1, max_id=0, min_id=0, hash=0
        ))
    except Exception:
        msg_info = None

    first_msg_valid = bool(msg_info and msg_info.messages and msg_info.messages[0].id == 1)
    creator_valid = first_msg_valid and bool(msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = msg_info.users[0].first_name if creator_valid else "حساب محذوف"
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (msg_info.messages[0].action.title if first_msg_valid and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom) and msg_info.messages[0].action.title != chat_title else None)

    description = chat_info.full_chat.about
    members = getattr(chat_info.full_chat, "participants_count", getattr(chat_obj_info, "participants_count", None))
    admins = getattr(chat_info.full_chat, "admins_count", None)
    banned_users = getattr(chat_info.full_chat, "kicked_count", None)
    restricted_users = getattr(chat_info.full_chat, "banned_count", None)
    members_online = getattr(chat_info.full_chat, "online_count", 0)
    messages_sent = getattr(chat_info.full_chat, "read_inbox_max_id", None)
    exp_count = getattr(chat_info.full_chat, "pts", None)
    username = f"@{chat_obj_info.username}" if getattr(chat_obj_info, "username", None) else None
    slowmode = "نعم" if getattr(chat_obj_info, "slowmode_enabled", False) else "لا"
    slowmode_time = getattr(chat_info.full_chat, "slowmode_seconds", None)
    restricted = "نعم" if getattr(chat_obj_info, "restricted", False) else "لا"
    verified = "نعم" if getattr(chat_obj_info, "verified", False) else "لا"

    try:
        participants_admins = await event.client(functions.channels.GetParticipantsRequest(
            channel=chat_obj_info.id, filter=types.ChannelParticipantsAdmins(), offset=0, limit=0, hash=0
        ))
        admins = participants_admins.count if participants_admins else admins
    except Exception:
        pass

    caption = f"المعرف: <code>{chat_obj_info.id}</code>\n"
    if chat_title:
        caption += f"اسم {chat_type}: {chat_title}\n"
    if former_title:
        caption += f"الاسم السابق: {former_title}\n"
    caption += f"نوع {chat_type}: {'عامة' if username else 'خاصة'}\n"
    if username:
        caption += f"الرابط: {username}\n"
    if creator_valid:
        caption += f"المنشئ: <a href=\"tg://user?id={creator_id}\">{creator_firstname}</a>\n"
    if created:
        caption += f"تاريخ الإنشاء: <code>{created.strftime('%b %d, %Y - %H:%M:%S')}</code>\n"
    if exp_count:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"المستوى: <code>{chat_level}</code>\n"
    if messages_sent:
        caption += f"الرسائل المرسلة: <code>{messages_sent}</code>\n"
    if members:
        caption += f"الأعضاء: <code>{members}</code>\n"
    if admins:
        caption += f"المشرفون: <code>{admins}</code>\n"
    if members_online:
        caption += f"الأعضاء المتصلون: <code>{members_online}</code>\n"
    if restricted_users:
        caption += f"الأعضاء المقيدون: <code>{restricted_users}</code>\n"
    if banned_users:
        caption += f"الأعضاء المحظورون: <code>{banned_users}</code>\n"
    caption += f"الوضع البطيء: {slowmode}"
    if slowmode_time:
        caption += f", <code>{slowmode_time}s</code>\n"
    caption += f"تم التحقق: {verified}\n"
    if description:
        caption += f"الوصف:\n<code>{description}</code>\n"

    try:
        await event.edit(caption, parse_mode="html")
    except Exception:
        await event.edit("حدث خطأ غير متوقع.")