import asyncio

from core.client import client
from core.bot_client import bot

try:
    from telethon import functions, types
except Exception:
    functions = None
    types = None


async def _brand_bot():
    # Wait a bit for both clients to be fully connected
    await asyncio.sleep(2.0)
    if bot is None or functions is None or types is None:
        return
    try:
        # Get owner (user) first name
        me = await client.get_me()
        owner_name = (getattr(me, "first_name", None) or "").strip() or "FLEX"

        display_name = f"البوت المساعد ل {owner_name}"
        about = "البوت المساعد لسورس فليك الاقوى"

        # Use MTProto to set bot info (name/about). Works only for bot accounts.
        await bot(functions.bots.SetBotInfo(
            bot=types.InputUserSelf(),  # the bot itself
            lang_code="",
            name=display_name,
            about=about,
            description=None
        ))
    except Exception as e:
        # Don't break anything if it fails; just log to stdout.
        print(f"[bot_branding] Failed to set bot branding: {e}")


# Schedule branding task on import if bot is available
if bot is not None:
    try:
        asyncio.get_event_loop().create_task(_brand_bot())
    except Exception as e:
        print(f"[bot_branding] Failed to schedule branding task: {e}")