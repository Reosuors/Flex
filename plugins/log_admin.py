from telethon import events
from telethon.tl.functions.channels import EditPhotoRequest as ChannelEditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto

from core.client import client
from core.error_reporting import ensure_log_group, _pick_photo_path


@client.on(events.NewMessage(from_users='me', pattern=r'\.(?:تحديث_صورة_السجل|set_log_photo)$'))
async def update_log_photo_default(event):
    """
    Update log group photo using local file (log_group.jpg preferred, else flex.jpg).
    """
    await event.delete()
    gid = await ensure_log_group()
    path = _pick_photo_path()
    if not path:
        await client.send_message(event.chat_id, "لا يوجد ملف log_group.jpg أو flex.jpg في مجلد السورس. أو قم بالرد على صورة واستخدم الأمر: .تحديث_صورة_السجل_بالرد", reply_to=event.message.id if event.message else None)
        return
    try:
        uploaded = await client.upload_file(path)
        await client(ChannelEditPhotoRequest(
            channel=gid,
            photo=InputChatUploadedPhoto(file=uploaded, video=None, video_start_ts=None)
        ))
        await client.send_message(event.chat_id, "✓ تم تحديث صورة قروب السجل (من الملف المحلي).")
    except Exception as e:
        await client.send_message(event.chat_id, f"تعذر تحديث الصورة: {e}")


@client.on(events.NewMessage(from_users='me', pattern=r'\.(?:تحديث_صورة_السجل_بالرد|set_log_photo_reply)$'))
async def update_log_photo_by_reply(event):
    """
    Update log group photo from replied media.
    """
    if not event.is_reply:
        await event.edit("يرجى الرد على صورة ثم استخدام الأمر.")
        return
    reply = await event.get_reply_message()
    try:
        gid = await ensure_log_group()
        # Download media to bytes then upload
        data = await client.download_media(reply, bytes)
        uploaded = await client.upload_file(data)
        await client(ChannelEditPhotoRequest(
            channel=gid,
            photo=InputChatUploadedPhoto(file=uploaded, video=None, video_start_ts=None)
        ))
        await event.edit("✓ تم تحديث صورة قروب السجل من الصورة التي تم الرد عليها.")
    except Exception as e:
        await event.edit(f"تعذر تحديث الصورة: {e}")