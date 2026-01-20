import asyncio
import random
from collections import deque
from telethon import events
from telethon.tl.types import InputMediaDice
from core.client import client

DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"

# أحكام (Truth/Dare) – قائمة خفيفة ومحترمة للاستخدام في المجموعات
DARES = [
    "اذكر اسم أول شخص خطر ببالك الآن!",
    "صف نفسك بكلمتين فقط.",
    "غيّر اسمك لمدة 10 دقائق إلى لقب يختاره لك أحد الأعضاء.",
    "أرسل آخر صورة في معرضك (إن كانت مناسبة).",
    "اكتب رسالة إيجابية لشخص في المجموعة واذكر اسمه.",
    "غيّر صورتك الشخصية لمدة 5 دقائق.",
    "ارسل أغنية تحبها مع سبب حبك لها.",
    "اكتب أكثر موقف محرج لك لكن بدون تفاصيل محرجة.",
    "أرسل إيموجي يعبّر عن مزاجك الآن مع سبب بسيط.",
    "اكتب هدفًا تريد تحقيقه هذا الأسبوع.",
]

TRUTHS = [
    "ما هو أكثر شيء تخشاه؟",
    "من هو أقرب شخص لك؟",
    "ما هي أكبر نقطة قوة في شخصيتك؟",
    "ما هو حلمك الذي تعمل عليه الآن؟",
    "ما أكثر عادة تريد التخلص منها؟",
    "هل تفضّل العزلة أم الاجتماعات؟ ولماذا؟",
    "ما هي أغرب عادة لديك؟",
    "لو بإمكانك نصيحة لنفسك قبل سنة، ماذا تقول؟",
    "أكثر موقف أسعدك هذا الشهر؟",
    "ما الشيء الذي لا يعرفه معظم الناس عنك؟",
]


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

# ألعاب أحكام
@client.on(events.NewMessage(pattern=r"\.احكام$"))
async def ahkam(event):
    msg = (
        "【 لعبة أحكام 】\n"
        "اختر:\n"
        "• .حكم  → مهمة/تحدّي بسيط وعفوي\n"
        "• .حقيقة → سؤال الحقيقة\n"
        "\nنصيحة: استخدمها بأسلوب محترم ولطيف في المجموعة."
    )
    await event.edit(msg)

@client.on(events.NewMessage(pattern=r"\.حكم$"))
async def random_dare(event):
    dare = random.choice(DARES)
    await event.edit(f"🎲 حكمك:\n{dare}")

@client.on(events.NewMessage(pattern=r"\.حقيقة$"))
async def random_truth(event):
    truth = random.choice(TRUTHS)
    await event.edit(f"📝 حقيقة:\n{truth}")