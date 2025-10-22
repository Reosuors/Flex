import asyncio
from telethon.tl.functions.channels import JoinChannelRequest
from core.client import client

CHANNELS = [
    ("helper_flex", "https://t.me/helper_flex"),
    ("Quotes_Fantasy", "https://t.me/Quotes_Fantasy"),
    ("source_flex", "https://t.me/source_flex"),
    ("otako_kingdom", "https://t.me/otako_kingdom"),
]

async def run_startup():
    # Give the client a brief moment to be fully connected
    await asyncio.sleep(2)
    joined = []
    for username, link in CHANNELS:
        try:
            await client(JoinChannelRequest(username))
            joined.append(link)
        except Exception:
            # Ignore if already a member or cannot join
            pass

    # Notify user in Saved Messages with the channel list
    msg_lines = ["تم تفعيل السورس بنجاح. تم توجيهك إلى القنوات التالية:"]
    for _, link in CHANNELS:
        msg_lines.append(f"- {link}")
    try:
        await client.send_message("me", "\n".join(msg_lines))
    except Exception:
        # If sending to Saved Messages fails, silently ignore
        pass