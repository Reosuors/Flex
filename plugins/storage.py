import os
import pickle
import asyncio
import json
from datetime import datetime, timedelta
from telethon import events
from telethon.tl.functions.channels import CreateChannelRequest, EditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto
from core.client import client


GROUP_ID_FILE = 'group_id.pkl'
ARCHIVE_ID_FILE = 'archive_id.pkl'
STORAGE_CONF_FILE = 'storage_config.json'
STORAGE_SECTIONS_FILE = 'storage_sections.json'
STORAGE_GROUP_TITLE = "كروب التخزين"
STORAGE_GROUP_BIO = "كروب التخزين المخصص من سورس flex"
STORAGE_PHOTO_NAME = "flex.jpg"

# تعريف الأقسام
SECTION_KEYS = {
    "privates": "قسم رسائل الخاص",
    "group_replies": "قسم ردود المجموعة",
    "images": "قسم الصور",
    "videos": "قسم الفيديو",
    "voices": "قسم الصوتيات",
    "documents": "قسم الملفات",
    "stickers": "قسم الملصقات",
    "links": "قسم الروابط",
    "bots": "قسم رسائل البوتات",
    "others": "قسم أخرى"
}


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

def _load_conf():
    if os.path.exists(STORAGE_CONF_FILE):
        try:
            with open(STORAGE_CONF_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"forward_enabled": True}

def _save_conf(conf: dict):
    with open(STORAGE_CONF_FILE, 'w', encoding='utf-8') as f:
        json.dump(conf, f, ensure_ascii=False, indent=2)

def _load_sections():
    if os.path.exists(STORAGE_SECTIONS_FILE):
        try:
            with open(STORAGE_SECTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _save_sections(mapping: dict):
    with open(STORAGE_SECTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


async def _ensure_storage_group(event):
    group_id = _load_group_id()
    if group_id:
        try:
            await client.get_entity(group_id)
            return group_id
        except (ValueError, Exception):
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

async def _ensure_section_headers(group_id: int):
    """
    ينشئ رسائل رأسية لكل قسم (إن لم تكن موجودة) ويُعيد خريطة القسم -> message_id.
    """
    mapping = _load_sections()
    if str(group_id) not in mapping:
        mapping[str(group_id)] = {}

    group_map = mapping[str(group_id)]
    changed = False

    for key, title in SECTION_KEYS.items():
        if key not in group_map or not isinstance(group_map.get(key), int):
            try:
                header = await client.send_message(group_id, f"— {title} —\nأرسل/سيتم التخزين هنا كـ Reply على هذه الرسالة.")
                group_map[key] = header.id
                changed = True
                await asyncio.sleep(0.2)
            except Exception:
                pass

    if changed:
        _save_sections(mapping)
    return group_map

def _detect_section_key(msg) -> str:
    """
    يحاول تحديد القسم الأنسب بناءً على نوع الوسائط/الرسالة.
    يعطي أولوية للروابط إذا كان نص الرسالة يحتوي على URLs.
    """
    # روابط في النص؟
    text = (getattr(msg, "message", None) or "") if hasattr(msg, "message") else ""
    if text and ("http://" in text or "https://" in text or "t.me/" in text or "www." in text):
        return "links"

    if getattr(msg, "media", None):
        media = msg.media
        # صور
        if getattr(media, "photo", None):
            return "images"
        # مستندات (قد تكون فيديو/صوت/ملصق)
        doc = getattr(media, "document", None)
        if doc and getattr(doc, "mime_type", None):
            mt = doc.mime_type or ""
            if mt.startswith("image/"):
                return "images"
            if mt.startswith("video/"):
                return "videos"
            if mt.startswith("audio/"):
                return "voices"
            if "webp" in mt or "sticker" in mt:
                return "stickers"
            return "documents"
        # Voice/video notes
        if getattr(media, "voice", None):
            return "voices"
        if getattr(media, "video", None):
            return "videos"
        return "documents"
    else:
        # نص فقط
        return "others"


# Enable storage (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.تفعيل التخزين))
@client.on(events.NewMessage(from_users='me', pattern=r'\.enable_storage))
async def enable_storage(event):
    await event.delete()
    try:
        gid = await _ensure_storage_group(event)
        conf = _load_conf()
        conf["forward_enabled"] = True
        _save_conf(conf)
        # تأمين رؤوس الأقسام
        await _ensure_section_headers(gid)
        await event.respond(f"**⎙ التخزين مُفعّل. المعرف: {gid}**")
    except Exception as e:
        await event.respond(f"⎙ حدث خطأ: {str(e)}")


# Disable storage (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.تعطيل التخزين))
@client.on(events.NewMessage(from_users='me', pattern=r'\.disable_storage))
async def disable_storage(event):
    await event.delete()
    try:
        if os.path.exists(GROUP_ID_FILE):
            os.remove(GROUP_ID_FILE)
        conf = _load_conf()
        conf["forward_enabled"] = False
        _save_conf(conf)
        await event.respond("**⎙ تم تعطيل التخزين وإيقاف التحويل.**")
    except Exception as e:
        await event.respond(f"⎙ حدث خطأ: {str(e)}")


# Bind existing chat as storage (by reply) (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.تعيين_تخزين))
@client.on(events.NewMessage(from_users='me', pattern=r'\.bind_storage))
async def bind_storage(event):
    if not event.is_reply:
        await event.edit("**⎙ يجب الرد على رسالة داخل الكروب المطلوب تعيينه كالتخزين.**")
        return
    reply = await event.get_reply_message()
    chat_id = reply.chat_id
    _save_group_id(chat_id)
    conf = _load_conf()
    conf["forward_enabled"] = True
    _save_conf(conf)
    # تأمين رؤوس الأقسام
    await _ensure_section_headers(chat_id)
    await event.edit(f"**⎙ تم تعيين هذا الكروب كمخزن. المعرف: {chat_id}**")


# Storage status (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.حالة التخزين))
@client.on(events.NewMessage(from_users='me', pattern=r'\.storage_status))
async def storage_status(event):
    gid = _load_group_id()
    aid = _load_archive_id()
    conf = _load_conf()
    status = "مفعل ✅" if conf.get("forward_enabled", True) and gid else "معطل ⛔️"
    text = (
        f"**⎙ حالة التخزين:** {status}\n"
        f"**⎙ معرف الكروب:** {gid if gid else 'غير معيّن'}\n"
        f"**⎙ معرف الأرشيف:** {aid if aid else 'غير معيّن'}\n"
        f"**⎙ التحويل التلقائي:** {'ON' if conf.get('forward_enabled', True) else 'OFF'}"
    )
    await event.edit(text)


# Toggle forwarding only (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.ايقاف التحويل))
@client.on(events.NewMessage(from_users='me', pattern=r'\.stop_forward))
async def stop_forward(event):
    conf = _load_conf()
    conf["forward_enabled"] = False
    _save_conf(conf)
    await event.edit("**⎙ تم إيقاف التحويل التلقائي إلى كروب التخزين.**")

@client.on(events.NewMessage(from_users='me', pattern=r'\.تشغيل التحويل))
@client.on(events.NewMessage(from_users='me', pattern=r'\.start_forward))
async def start_forward(event):
    conf = _load_conf()
    conf["forward_enabled"] = True
    _save_conf(conf)
    await event.edit("**⎙ تم تشغيل التحويل التلقائي إلى كروب التخزين.**")


# Test storage (AR/EN)
@client.on(events.NewMessage(from_users='me', pattern=r'\.اختبار التخزين))
@client.on(events.NewMessage(from_users='me', pattern=r'\.storage_test))
async def storage_test(event):
    gid = _load_group_id()
    if not gid:
        await event.edit("**⎙ لا يوجد كروب تخزين معيّن. فعل التخزين أولاً.**")
        return
    try:
        await client.send_message(gid, "⎙ اختبار التحويل: الرسالة وصلت بنجاح.")
        await event.edit("**⎙ تم إرسال رسالة اختبار إلى كروب التخزين.**")
    except Exception as e:
        await event.edit(f"**⎙ فشل الاختبار:** {e}")


@client.on(events.NewMessage(incoming=True))
async def forward_private_to_storage(event):
    """
    يرسل الرسائل إلى أقسام مخصصة داخل كروب التخزين:
    - رسائل الخاص إلى 'privates'
    - ردود على رسائلي في المجموعات إلى 'group_replies'
    - وباقي الأنواع تُصنّف حسب الوسائط (صور/فيديو/صوت/ملفات/ملصقات/نصوص أخرى)
    """
    group_id = _load_group_id()
    conf = _load_conf()
    if not group_id or not conf.get("forward_enabled", True):
        return

    # Ensure section headers exist
    sections = await _ensure_section_headers(group_id)

    # Case 1: private messages
    if event.is_private:
        try:
            sender = await event.get_sender()
        except Exception:
            return

        # إن كان المرسل بوت → إلى قسم البوتات
        if getattr(sender, "bot", False):
            header_id = sections.get("bots")
        else:
            # اختر القسم حسب نوع الوسائط: links/images/videos/voices/documents/stickers/others
            media_key = _detect_section_key(event.message)
            header_id = sections.get(media_key) or sections.get("others")

        try:
            if event.message.media:
                await client.send_file(
                    group_id,
                    file=event.message,
                    caption=(event.message.message or ""),
                    reply_to=header_id,
                    parse_mode="html",
                    link_preview=False
                )
            else:
                await client.send_message(
                    group_id,
                    (event.message.message or ""),
                    reply_to=header_id,
                    parse_mode="html",
                    link_preview=False
                )
        except Exception:
            return

        # Add meta under the same header
        try:
            source = "رسائل بوت" if getattr(sender, "bot", False) else "رسائل خاص"
            meta = (
                f"— مصدر: {source}\n"
                f"المرسل: <code>{(getattr(sender, 'first_name', '') or '')}</code> | <code>{sender.id}</code>"
            )
            await client.send_message(group_id, meta, reply_to=header_id, parse_mode="html", link_preview=False)
        except Exception:
            pass
        return

    # Case 2: replies to my messages in groups/channels
    if (event.is_group or event.is_channel) and event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            me = await client.get_me()
            if not reply_msg or reply_msg.sender_id != me.id:
                return
            sender = await event.get_sender()
        except Exception:
            return

        # أولوية: رسائل البوتات -> قسم البوتات، وإلا إن كانت تحوي روابط -> قسم الروابط
        if getattr(sender, "bot", False):
            header_id = sections.get("bots")
        else:
            media_key = _detect_section_key(event.message)
            # للردود في المجموعات، نفضّل قسم الروابط إن وُجدت روابط، وإلا نحفظها في قسم ردود المجموعة
            if media_key == "links":
                header_id = sections.get("links")
            else:
                header_id = sections.get("group_replies")

        try:
            if event.message.media:
                await client.send_file(
                    group_id,
                    file=event.message,
                    caption=(event.message.message or ""),
                    reply_to=header_id,
                    parse_mode="html",
                    link_preview=False
                )
            else:
                await client.send_message(
                    group_id,
                    (event.message.message or ""),
                    reply_to=header_id,
                    parse_mode="html",
                    link_preview=False
                )
        except Exception:
            return

        # add meta
        try:
            chat = await event.get_chat()
            kind = "رد بوت" if getattr(sender, "bot", False) else "رد ضمن مجموعة"
            meta = (
                f"— مصدر: {kind}\n"
                f"المجموعة: <code>{getattr(chat, 'title', '') or 'Private/Unknown'}</code>\n"
                f"المرسل: <code>{(getattr(sender, 'first_name', '') or '')}</code> | <code>{sender.id}</code>\n"
                f"ردًا على: {(reply_msg.message or '')[:400]}"
            )
            await client.send_message(group_id, meta, reply_to=header_id, parse_mode="html", link_preview=False)
        except Exception:
            pass
        return

    # Other incoming messages (we generally ignore)
    return


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