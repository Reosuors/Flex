import asyncio
import random
from telethon import events, functions
from core.client import client

hunting_active = False
hunting_pattern = ""
channel_id = None
hunting_attempts = 0

def generate_username(pattern):
    username = ""
    for char in pattern:
        if char in ["H", "B"]:
            username += random.choice("abcdefghijklmnopqrstuvwxyz")
        elif char == "4":
            username += random.choice("0123456789")
        else:
            username += char
    return username

def get_pattern_by_type(hunt_type):
    patterns = {
        "ثلاثي1": "H_B_H",
        "خماسي ارقام": "HB444",
        "ثلاثي2": "H_4_B",
        "ثلاثي3": "H_4_0",
        "رباعي1": "HHH_B",
        "رباعي2": "H_BBB",
        "رباعي3": "HH_BB",
        "رباعي4": "HH_HB",
        "رباعي5": "HH_BH",
        "رباعي6": "HB_BH",
        "رباعي7": "HB_HB",
        "رباعي8": "HB_BB",
        "شبه رباعي1": "H_H_H_B",
        "شبه رباعي2": "H_B_B_B",
        "شبه رباعي3": "H_BB_H",
        "شبه رباعي4": "H_BB_B",
        "خماسي حرفين1": "HHHBR",
        "خماسي حرفين2": "H4BBB",
        "خماسي حرفين3": "HBBBR",
        "سداسي_حرفين1": "HBHHHB",
        "سداسي_حرفين2": "HHHHBB",
        "سداسي_حرفين3": "HHHBBH",
        "سداسي_حرفين4": "HHBBHH",
        "سداسي_حرفين5": "HBBHHH",
        "سداسي_حرفين6": "HHBBBB",
        "سداسي_شرطه": "HHHH_B",
        "سباعيات1": "HHHHHHB",
        "سباعيات2": "HHHHHBH",
        "سباعيات3": "HHHHBHH",
        "سباعيات4": "HHHBHHH",
        "سباعيات5": "HHBHHHH",
        "سباعيات6": "HBHHHHH",
        "سباعيات7": "HBBBBBB",
        "بوتات1": "HB_Bot",
        "بوتات2": "H_BBot",
        "بوتات3": "HB4Bot",
        "بوتات4": "H4BBot",
        "بوتات5": "H44Bot",
        "بوتات6": "HRBBot",
        "بوتات7": "HHBBot",
        "بوتات8": "HHBBot",
        "بوتات9": "HH4Bot"
    }
    return patterns.get(hunt_type, hunt_type)

async def create_channel():
    global channel_id
    try:
        result = await client(functions.channels.CreateChannelRequest(
            title="صيد سورس HUNTER",
            about="قناه لصيد اليوزرات تابعه لسورس HUNTER",
            megagroup=False
        ))
        if result.chats:
            channel_id = result.chats[0].id
            return channel_id
    except Exception:
        pass
    return None

async def set_channel_username(username):
    global channel_id
    if channel_id is not None:
        try:
            await client(functions.channels.UpdateUsernameRequest(
                channel=channel_id, username=username
            ))
            return True
        except Exception:
            return False
    return False

@client.on(events.NewMessage(pattern=r"\.صيد (.+)"))
async def start_hunting(event):
    global hunting_active, hunting_pattern, hunting_attempts, channel_id

    if hunting_active:
        await event.edit("الصيد قيد التشغيل بالفعل!")
        return

    hunt_type = event.pattern_match.group(1)
    hunting_pattern = get_pattern_by_type(hunt_type)
    hunting_active = True
    hunting_attempts = 0

    await event.edit(f"**⎉╎تم بـدء الصيـد .. بنجـاح ☑️\n ⎉╎علـى النـوع {hunting_pattern}\n ⎉╎لمعرفـة حالة عمليـة الصيـد ( `.حالة الصيد` )\n⎉╎لـ ايقـاف عمليـة الصيـد ( `.ايقاف الصيد`  )**")

    channel_id = await create_channel()
    if not channel_id:
        await event.reply("**فشل إنشاء القناة، تأكد من صحة البيانات.**")
        hunting_active = False
        return

    while hunting_active:
        username = generate_username(hunting_pattern)
        hunting_attempts += 1
        try:
            result = await client(functions.account.CheckUsernameRequest(username))
            if result:
                success = await set_channel_username(username)
                if success:
                    await event.respond(f"تم حجز اليوزر بنجاح: @{username}")
                    hunting_active = False
                    break
                else:
                    await event.respond(f"اليوزر @{username} متاح لكنه لم يُعين للقناة.")
        except Exception:
            pass
        await asyncio.sleep(2)

@client.on(events.NewMessage(pattern=r"\.ايقاف الصيد"))
async def stop_hunting(event):
    global hunting_active
    hunting_active = False
    await event.edit("تم إيقاف الصيد.")

@client.on(events.NewMessage(pattern=r"\.حالة الصيد"))
async def hunting_status(event):
    status = "⎙ قيد التشغيل" if hunting_active else "⎙ متوقف"
    await event.edit(f"⎙ حالة الصيد: {status}\n⎙ عدد المحاولات: {hunting_attempts}")