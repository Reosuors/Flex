import os
import pickle
import traceback
from typing import Optional, Callable, Any

from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.channels import EditPhotoRequest as ChannelEditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto

from core.client import client


LOG_GROUP_TITLE = "قروب السجل"
LOG_GROUP_BIO = "سجل أخطاء الأوامر — يتم الإبلاغ هنا عن أي خطأ يحصل أثناء تنفيذ الأوامر."
LOG_GROUP_ID_FILE = "log_group_id.pkl"
LOG_PHOTO_NAME = "flex.jpg"  # إن وجدت سنضعها صورة للمجموعة


def _load_log_group_id() -> Optional[int]:
    if os.path.exists(LOG_GROUP_ID_FILE):
        try:
            with open(LOG_GROUP_ID_FILE, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None
    return None


def _save_log_group_id(group_id: int) -> None:
    with open(LOG_GROUP_ID_FILE, "wb") as f:
        pickle.dump(group_id, f)


async def ensure_log_group() -> int:
    """
    Ensure the log group exists and return its chat id.
    Creates a mega-group named LOG_GROUP_TITLE if missing.
    """
    gid = _load_log_group_id()
    if gid:
        # verify it still exists
        try:
            await client.get_entity(gid)
            return gid
        except Exception:
            try:
                os.remove(LOG_GROUP_ID_FILE)
            except Exception:
                pass

    # Create new megagroup for logging
    result = await client(CreateChannelRequest(
        title=LOG_GROUP_TITLE,
        about=LOG_GROUP_BIO,
        megagroup=True
    ))
    channel = result.chats[0]
    gid = channel.id

    # Set photo if available (best-effort)
    if os.path.exists(LOG_PHOTO_NAME):
        try:
            uploaded = await client.upload_file(LOG_PHOTO_NAME)
            await client(ChannelEditPhotoRequest(
                channel=channel,
                photo=InputChatUploadedPhoto(file=uploaded, video=None, video_start_ts=None)
            ))
        except Exception:
            # ignore setting photo errors
            pass

    _save_log_group_id(gid)
    return gid


async def report_command_error(event, func: Callable, err: BaseException) -> None:
    """
    Send a detailed error report to the log group.
    """
    try:
        gid = await ensure_log_group()
    except Exception:
        # If we cannot ensure the group, there's nothing we can do
        return

    # Collect context
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, "title", None) or getattr(chat, "first_name", None) or "Private/Unknown"
        chat_id = getattr(chat, "id", None)
    except Exception:
        chat_title = "Unknown"
        chat_id = None

    try:
        sender = await event.get_sender()
        sender_name = getattr(sender, "first_name", None) or getattr(sender, "username", None) or "Unknown"
        sender_id = getattr(sender, "id", None)
    except Exception:
        sender_name = "Unknown"
        sender_id = None

    raw_text = ""
    try:
        raw_text = getattr(event, "raw_text", None) or (getattr(event, "message", None) and getattr(event.message, "message", "")) or ""
    except Exception:
        raw_text = ""

    func_name = getattr(func, "__name__", "unknown_handler")
    tb = "".join(traceback.format_exception(type(err), err, err.__traceback__))[-3500:]

    # Arabic report message as requested
    msg = (
        "تنبيه: هذا الأمر لم يعمل.\n"
        f"• النص: {raw_text or '—'}\n"
        f"• الدالة: {func_name}\n"
        f"• المحادثة: {chat_title} | {chat_id}\n"
        f"• المرسل: {sender_name} | {sender_id}\n"
        "• الخطأ بالتفصيل:\n"
        f"<code>{tb}</code>\n\n"
        "الرجاء إرسال هذه الرسالة للمطور @MRM_U لكي يتم حل الخطأ."
    )

    try:
        await client.send_message(gid, msg, parse_mode="html", link_preview=False)
    except Exception:
        # last resort: ignore
        pass


def patch_client_error_reporting() -> None:
    """
    Monkey-patch client.on to wrap all handlers with a try/except
    that reports errors to the log group.
    """
    original_on = client.on

    def on_wrapper(*on_args, **on_kwargs):
        decorator = original_on(*on_args, **on_kwargs)

        def _decorator(func: Callable[..., Any]):
            async def wrapped(event, *_a, **_kw):
                try:
                    return await func(event, *_a, **_kw)
                except Exception as e:
                    try:
                        await report_command_error(event, func, e)
                    finally:
                        # re-raise so Telethon can log as well
                        raise
            return decorator(wrapped)

        return _decorator

    # apply patch once
    if not getattr(client, "_error_reporting_patched", False):
        setattr(client, "_error_reporting_patched", True)
        client.on = on_wrapper  # type: ignore[attr-defined]