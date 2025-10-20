import os
import pickle
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest, EditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto
from core.client import client


GROUP_ID_FILE = 'group_id.pkl'
STORAGE_GROUP_TITLE = "كروب التخزين"
STORAGE_GROUP_BIO = "كروب التخزين المخصص من سورس flex"
STORAGE_PHOTO_NAME = "flex.jpg"


def _load_group_id():
    if os.path.exists(GROUP_ID_FILE):
        with open(GROUP_ID_FILE, 'rb') as f:
            return pickle.load(f)
    return None


def _save_group_id(group_id: int):
    with open(GROUP_ID_FILE, 'wb') as f:
        pickle.dump(group_id, f)


async def _ensure_storage_group(event):
    group_id = _load_group_id()
    if group_id:
        try:
            await client.get_entity(group_id)
            return group_id
        except ValueError:
            # stale id, recreate
            os.remove(GROUP_ID_FILE)

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


@client.on(events.NewMessage(from_users='me', pattern='.تفعيل التخزين'))
async def enable_storage(event):
    await event.delete()
    try:
        if event.is_group:
            await event.reply("**⎙ الكروب موجود بالفعل. سيتم تفعيل الكود في الكروب السابق.**")
            return
        elif event.is_private:
            await _ensure_storage_group(event)
    except Exception as e:
        await event.reply(f"⎙ حدث خطأ: {str(e)}")


@client.on(events.NewMessage(incoming=True))
async def forward_private_to_storage(event):
    # Forward incoming private messages to storage group if configured
    group_id = _load_group_id()
    if not group_id:
        return

    if event.is_private and not (await event.get_sender()).bot:
        await client.forward_messages(group_id, event.message)
        # Optional: add simple meta
        sender = await event.get_sender()
        meta = f"#التــاكــات\n\n⌔┊المستخدم : <code>{sender.first_name}</code>\n⌔┊الرسالة : {(event.message.message or '')}"
        await client.send_message(group_id, meta, parse_mode="html", link_preview=False)


@client.on(events.NewMessage(from_users='me', pattern='.تعطيل التخزين'))
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