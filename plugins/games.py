import asyncio
from collections import deque
from telethon import events
from telethon.tl.types import InputMediaDice
from core.client import client

DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"


async def roll_dice(event, emoticon, max_value):
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()

    input_str = event.pattern_match.group(2)
    await event.delete()

    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))

    if input_str:
        try:
            required_number = int(input_str)
            while True:
                if r.media.value == required_number:
                    break
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except Exception:
            pass


@client.on(events.NewMessage(pattern=f"({DART_E_MOJI}|\\.سهم)( ([1-6])|$)"))
async def dart_game(event):
    emoticon = "🎯" if event.pattern_match.group(1) == ".سهم" else DART_E_MOJI
    await roll_dice(event, emoticon, 6)


@client.on(events.NewMessage(pattern=f"({DICE_E_MOJI}|\\.نرد)( ([1-6])|$)"))
async def dice_game(event):
    emoticon = "🎲" if event.pattern_match.group(1) == ".نرد" else DICE_E_MOJI
    await roll_dice(event, emoticon, 6)


@client.on(events.NewMessage(pattern=f"({BALL_E_MOJI}|\\.سله)( ([1-5])|$)"))
async def basketball_game(event):
    emoticon = "🏀" if event.pattern_match.group(1) == ".سله" else BALL_E_MOJI
    await roll_dice(event, emoticon, 5)


@client.on(events.NewMessage(pattern=f"({FOOT_E_MOJI}|\\.كرة)( ([1-5])|$)"))
async def football_game(event):
    emoticon = "⚽️" if event.pattern_match.group(1) == ".كرة" else FOOT_E_MOJI
    await roll_dice(event, emoticon, 5)


@client.on(events.NewMessage(pattern=f"({SLOT_E_MOJI}|\\.حظ)( ([1-64])|$)"))
async def slot_game(event):
    emoticon = "🎰" if event.pattern_match.group(1) == ".حظ" else SLOT_E_MOJI
    await roll_dice(event, emoticon, 64)


@client.on(events.NewMessage(pattern=r"\.gym$"))
async def gym(event):
    deq = deque(list("🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍"))
    for _ in range(48):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)