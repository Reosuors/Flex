import asyncio
from telethon import events
from telethon.tl.functions.messages import SetTypingRequest
from telethon.tl import types
from core.client import client

DEFAULT_SECONDS = 8
MIN_SECONDS = 2
MAX_SECONDS = 120

def clamp_seconds(n: int) -> int:
    return max(MIN_SECONDS, min(MAX_SECONDS, n or DEFAULT_SECONDS))

async def fake_action(chat_id, action_obj, seconds: int):
    seconds = clamp_seconds(seconds)
    # Re-send action every ~4 seconds to keep it active
    end = asyncio.get_event_loop().time() + seconds
    while asyncio.get_event_loop().time() < end:
        try:
            await client(SetTypingRequest(chat_id, action_obj))
        except Exception:
            # ignore failures, continue
            pass
        await asyncio.sleep(4)

# Arabic commands
@client.on(events.NewMessage(outgoing=True, pattern=r"\.يكتب(?:\s+(\d+))?$"))
async def fake_typing(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageTypingAction(), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يرفع_صورة(?:\s+(\d+))?$"))
async def fake_upload_photo(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageUploadPhotoAction(progress=10), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يرفع_ملف(?:\s+(\d+))?$"))
async def fake_upload_document(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageUploadDocumentAction(progress=10), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يرفع_فيديو(?:\s+(\d+))?$"))
async def fake_upload_video(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageUploadVideoAction(progress=10), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يرفع_صوت(?:\s+(\d+))?$"))
async def fake_upload_audio(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageUploadAudioAction(progress=10), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يسجل_فيديو(?:\s+(\d+))?$"))
async def fake_record_video(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageRecordVideoAction(), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يسجل_صوت(?:\s+(\d+))?$"))
async def fake_record_audio(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageRecordAudioAction(), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.اختيار_ملصق(?:\s+(\d+))?$"))
async def fake_choose_sticker(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageChooseStickerAction(), n)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يلعب(?:\s+(\d+))?$"))
async def fake_game_play(event):
    n = int(event.pattern_match.group(1) or DEFAULT_SECONDS)
    await event.delete()
    await fake_action(event.chat_id, types.SendMessageGamePlayAction(), n)

# English aliases will be rewritten by command_aliases.py (e.g., .typing -> .يكتب)