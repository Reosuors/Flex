import asyncio
import random
import re
from telethon import events, functions
from core.client import client

hunting_active = False
hunting_pattern = ""
channel_entity = None
hunting_attempts = 0

def generate_username(pattern):
    """
    Generate a candidate username from a pattern.
    H/B -> random lowercase letter
    4   -> random digit
    '_' -> underscore kept
    Other characters are kept as-is.
    Ensures first character is a letter (Telegram requirement).
    """
    username = ""
    for char in pattern:
        if char in ["H", "B"]:
            username += random.choice("abcdefghijklmnopqrstuvwxyz")
        elif char == "4":
            username += random.choice("0123456789")
        else:
            username += char

    # normalize: lowercase and ensure length bounds
    username = username.lower()

    # Username must start with a letter
    if not username or not username[0].isalpha():
        head = random.choice("abcdefghijklmnopqrstuvwxyz")
        tail = username[1:] if len(username) > 1 else ""
        username = head + tail

    # Telegram username rules: 5-32 chars, letters/digits/underscore
    username = re.sub(r"[^a-z0-9_]", "", username)
    if len(username) < 5:
        username = (username + "_____")[:5]
    elif len(username) > 32:
        username = username[:32]
    return username

def valid_candidate(u):
    # disallow 3+ consecutive identical chars
    if re.search(r"(.)\1\1", u):
        return False
    # require at least one letter and one digit if length >= 6
    if len(u) >= 6:
        if not re.search(r"[a-z]", u) or not re.search(r"[0-9]", u):
            return False
    # avoid ending with underscore
    if u.endswith("_"):
        return False
    # avoid double underscores
    if "__" in u:
        return False
    return True

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
        "خماسي حرفين1": "HHH_B",
        "خماسي حرفين2": "H4BBB",
        "خماسي حرفين3": "HBBB_",
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
        "بوتات1": "HB_bot",
        "بوتات2": "H_bbot",
        "بوتات3": "HB4bot",
        "بوتات4": "H4bbot",
        "بوتات5": "H44bot",
        "بوتات6": "HB_bbot",
        "بوتات7": "HHbbot",
        "بوتات8": "HHbbot",
        "بوتات9": "HH4bot"
    }
    return patterns.get(hunt_type, hunt_type)

async def create_channel():
    """
    Create a new channel for hunting and return its entity.
    """
    try:
        result = await client(functions.channels.CreateChannelRequest(
            title="صيد سورس HUNTER",
            about="قناه لصيد اليوزرات تابعه لسورس HUNTER",
            megagroup=False
        ))
        if result.chats:
            return result.chats[0]
    except Exception:
        pass
    return None

async def set_channel_username(username):
    """
    Update the channel's username. Requires the channel entity.
    """
    global channel_entity
    if channel_entity is not None:
        try:
            await client(functions.channels.UpdateUsernameRequest(
                channel=channel_entity, username=username
            ))
            return True
        except Exception:
            return False
    return False

@client.on(events.NewMessage(pattern=r"\.صيد (.+)"))
async def start_hunting(event):
    global hunting_active, hunting_pattern, hunting_attempts, channel_entity

    if hunting_active:
        await event.edit("الصيد قيد التشغيل بالفعل!")
        return

    hunt_type = event.pattern_match.group(1)
    hunting_pattern = get_pattern_by_type(hunt_type)
    hunting_active = True
    hunting_attempts = 0

    await event.edit(f"**⎉╎تم بـدء الصيـد .. بنجـاح ☑️\n ⎉╎علـى النـوع {hunting_pattern}\n ⎉╎لمعرفـة حالة عمليـة الصيـد ( `.حالة الصيد` )\n⎉╎لـ ايقـاف عمليـة الصيـد ( `.ايقاف الصيد`  )**")

    channel_entity = await create_channel()
    if not channel_entity:
        await event.reply("**فشل إنشاء القناة، تأكد من صحة البيانات.**")
        hunting_active = False
        return

    while hunting_active:
        username = generate_username(hunting_pattern)
        # apply validity filters
        if not valid_candidate(username):
            await asyncio.sleep(0.1)
            continue
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