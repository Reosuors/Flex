import time
from telethon import events
from telethon.tl.types import User, Chat, Channel, Dialog

from core.client import client


@client.on(events.NewMessage(outgoing=True, pattern=r"\.احصائياتي"))
async def stats_counts(event):
    start_time = time.time()
    u = g = c = bc = b = 0
    await event.edit("**⪼ جاري المعـالجه ༗.**")
    dialogs = await client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        current_entity = d.entity
        if isinstance(current_entity, User):
            if current_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(current_entity, Chat):
            g += 1
        elif isinstance(current_entity, Channel):
            if current_entity.broadcast:
                bc += 1
            else:
                c += 1
    result = ""
    result += f"ـ𓆩 ᯓ𝐒𝐎𝐔𝐑𝐂𝐄 𝐅𝑳𝐄𝐗 **- 🝢 - احصـائيـات الحسـاب** 𓆪\n"
    result += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
    result += f"**⎉╎المستخدمون :**\t**{u}**\n"
    result += f"**⎉╎المجموعات :**\t**{g}**\n"
    result += f"**⎉╎المجموعات الخارقه :**\t**{c}**\n"
    result += f"**⎉╎القنوات :**\t**{bc}**\n"
    result += f"**⎉╎البوتات :**\t**{b}**\n"
    result += f"ـ𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"
    stop_time = time.time() - start_time
    result += f"\n**- الوقـت المستغـرق 📟 :** {stop_time:.02f} **ثـانيـه**"
    await event.edit(result)


@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلوماتي"))
async def stats_details(event):
    cat = await event.edit("**⪼ جاري المعـالجه ༗.**...")
    start_time = time.time()
    private_chats = bots = groups = broadcast_channels = 0
    admin_in_groups = creator_in_groups = 0
    admin_in_broadcast_channels = creator_in_channels = 0
    unread_mentions = unread = 0

    def inline_mention(user):
        return f"[{user.first_name}](tg://user?id={user.id})"

    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (isinstance(entity, Channel) and entity.megagroup) or (
            not isinstance(entity, Channel) and not isinstance(entity, User) and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count

    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"ـ𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐅𝑳𝐄𝐗**- 🝢 - معلومات {full_name}** 𓆪\n"
    response += f"**ـ𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻**\n"
    response += f"**- الخـاص :** {private_chats} \n"
    response += f" ★ **اشخـاص :** `{private_chats - bots}` \n"
    response += f" ★ **بـوتـات :** `{bots}` \n"
    response += f"**- المجمـوعـات :** {groups} \n"
    response += f"**- القنـوات :** {broadcast_channels} \n"
    response += f"**- ادمـن في مجموعات :** {admin_in_groups} \n"
    response += f" ★ **مـالك :** `{creator_in_groups}` \n"
    response += f" ★ **ادمـن : ** `{admin_in_groups - creator_in_groups}` \n"
    response += f"**- ادمـن في قنـوات :** {admin_in_broadcast_channels} \n"
    response += f" ★ **مـالك :** `{creator_in_channels}` \n"
    response += f" ★ **ادمـن :** `{admin_in_broadcast_channels - creator_in_channels}` \n"
    response += f"**ـUnread:** {unread} \n"
    response += f"**ـUnread Mentions:** {unread_mentions} \n\n"
    response += f"📌**- الوقـت المستغـرق 📟 :** {stop_time:.02f} **ثـانيـه**"
    await cat.edit(response)