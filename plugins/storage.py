import os
import pickle
import asyncio
from datetime import datetime, timedelta
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest, EditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto
from core.client import client


GROUP_ID_FILE = 'group_id.pkl'
ARCHIVE_ID_FILE = 'archive_id.pkl'
STORAGE_GROUP_TITLE = "كروب التخزين"
STORAGE_GROUP_BIO = "كروب التخزين المخصص من سورس flex"
STORAGE_PHOTO_NAME = "flex.jpg"


def _load_id(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

def _save_id(path, value):
    with open(path, 'wb') as f:
        pickle.dump(value, f)

def _load_group_id():
    return _load_id(GROUP_ID_FILE)

def _save_group_id(group_id: int):
    _save_id(GROUP_ID_FILE, group_id)

def _load_archive_id():
    return _load_id(ARCHIVE_ID_FILE)

def _save_archive_id(chat_id: int):
    _save_id(ARCHIVE_ID_FILE, chat_id)


async def _ensure_storage_group(event):
    group_id = _load_group_id()
    if group_id:
        try:
            await client.get_entity(group_id)
            return group_id
        except (ValueError, Exception):
            # stale id, recreate
            try:
                os.remove(GROUP_ID_FILE)
            except Exception:
                pass

    # Create new megagroup
    result = await client(CreateChannelRequest(
        title=STORAGE_GROUP_TITLE,
        about=STORAGE_GROUP_BIO,
        megagroup=True
    ))
    channel = result.chats[0]
    group_id = channel.id

    # Set photo from repo root if exists
    if os.path.exists(STORAGE_PHOTO_NAME):
        try:
            uploaded_photo = await client.upload_file(STORAGE_PHOTO_NAME)
            await client(EditPhotoRequest(
                channel=channel,  # pass the channel entity, not the integer id
                photo=InputChatUploadedPhoto(
                    file=uploaded_photo,
                    video=None,
                    video_start_ts=None
                )
            ))
        except Exception as photo_error:
            print(f"[storage] Failed to set photo: {photo_error}")

    _save_group_id(group_id)
    await event.reply("**⎙ تم إنشاء كروب جديد وتعيينه لتخزين الرسائل الخاصة**")
    return group_id


@client.on(events.NewMessage(from_users='me', pattern=r'\.تفعيل التخزين))
async def enable_storage(event):
    await event.delete()
    try:
        if event.is_private:
            await _ensure_storage_group(event)
        else:
            await event.reply("**⎙ يفضل تشغيل الأمر من الخاص. سيتم التفعيل وإنشاء الكروب تلقائيًا.**")
            await _ensure_storage_group(event)
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {str(e)}")


@client.on(events.NewMessage(incoming=True))
async def forward_private_to_storage(event):
    # Forward incoming private messages to storage group if configured
    group_id = _load_group_id()
    if not group_id:
        return

    if event.is_private:
        try:
            sender = await event.get_sender()
            if getattr(sender, "bot", False):
                return
        except Exception:
            pass
        await client.forward_messages(group_id, event.message)
        # Optional: add simple meta
        try:
            sender = await event.get_sender()
            meta = f"#التــاكــات\n\n⌔┊المستخدم : <code>{sender.first_name}</code>\n⌔┊الرسالة : {(event.message.message or '')}"
            await client.send_message(group_id, meta, parse_mode="html", link_preview=False)
        except Exception:
            pass


@client.on(events.NewMessage(from_users='me', pattern=r'\.تعطيل التخزين))
async def disable_storage(event):
    await event.delete()
    try:
        if os.path.exists(GROUP_ID_FILE):
            os.remove(GROUP_ID_FILE)
            await event.reply("**⎙ تم تعطيل التخزين بنجاح.**")
        else:
            await event.reply("**⎙ التخزين غير مفعل بالفعل.**")
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {str(e)}")


# إعداد الأرشيف الذكي + أرشفة الوسائط الأقدم
@client.on(events.NewMessage(from_users='me', pattern=r'\.تعيين_ارشيف (\-?\d+)))
async def set_archive(event):
    chat_id = int(event.pattern_match.group(1))
    _save_archive_id(chat_id)
    await event.edit(f"✓ تم تعيين معرف الأرشيف إلى: {chat_id}")

@client.on(events.NewMessage(from_users='me', pattern=r'\.تعيين_ارشيف))
async def set_archive_by_reply(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        chat_id = reply.chat_id
        _save_archive_id(chat_id)
        await event.edit(f"✓ تم تعيين الأرشيف إلى محادثة الرد: {chat_id}")
    else:
        await event.edit("استخدم: .تعيين_ارشيف <id> أو بالرد على محادثة الأرشيف.")

@client.on(events.NewMessage(from_users='me', pattern=r'\.أرشفة (\d+)))
async def run_archive(event):
    group_id = _load_group_id()
    archive_id = _load_archive_id()
    if not group_id or not archive_id:
        await event.edit("⚠️ يجب تعيين كروب التخزين (.تفعيل التخزين) ومعرف الأرشيف (.تعيين_ارشيف <id>) أولًا.")
        return
    days = int(event.pattern_match.group(1))
    cutoff = datetime.utcnow() - timedelta(days=days)
    await event.edit(f"⎙ بدء الأرشفة: نقل الوسائط الأقدم من {days} يومًا إلى الأرشيف...")
    moved = 0
    async for msg in client.iter_messages(group_id, limit=1000):
        try:
            msg_date = msg.date.replace(tzinfo=None) if msg.date else None
            if msg_date and msg_date < cutoff and msg.media:
                await client.forward_messages(archive_id, msg)
                moved += 1
                await asyncio.sleep(0.15)
        except Exception:
            pass
    await event.edit(f"✓ تم أرشفة {moved} وسيط/وسائط إلى الأرشيف.")