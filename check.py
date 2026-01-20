import os
import json
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from core.client import client

# Default remote URLs (can be overridden by env vars)
DEFAULT_AR_URL = "https://files.catbox.moe/fcqmhx.jpeg"
DEFAULT_EN_URL = "https://files.catbox.moe/sdzlav.jpeg"

MAX_VIDEO_SECONDS = 10 * 60  # 10 minutes

def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def project_file(*parts: str) -> str:
    return os.path.abspath(os.path.join(project_root(), *parts))

# Persistent config for custom media (image or video)
CFG_PATH = project_file("check_images.json")

def _load_cfg() -> dict:
    if not os.path.exists(CFG_PATH) or os.stat(CFG_PATH).st_size == 0:
        return {"ar": "", "en": ""}
    try:
        with open(CFG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("ar", "")
            data.setdefault("en", "")
            return data
    except Exception:
        return {"ar": "", "en": ""}

def _save_cfg(data: dict) -> None:
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

CFG = _load_cfg()

def resolve_media(candidates: list[str], env_var: str, default_url: str | None = None, cfg_key: str | None = None) -> str | None:
    """
    Priority:
    1) Explicitly saved path/url in config (CFG[cfg_key]) if provided.
    2) First existing local file from candidates.
    3) URL from env var.
    4) Default URL.
    Works for image or video alike.
    """
    if cfg_key:
        cfg_val = (CFG.get(cfg_key) or "").strip()
        if cfg_val:
            if (cfg_val.startswith("http://") or cfg_val.startswith("https://")) or os.path.exists(cfg_val):
                return cfg_val
    for p in candidates:
        if p and os.path.exists(p):
            return p
    url = os.environ.get(env_var) or default_url
    if url:
        return url
    return None

def _is_video_message(msg) -> tuple[bool, int]:
    """
    Return (is_video, duration_seconds) for replied media, else (False, 0).
    """
    media = getattr(msg, "media", None)
    doc = getattr(media, "document", None) if media else None
    if doc and getattr(doc, "attributes", None):
        for attr in doc.attributes:
            if isinstance(attr, DocumentAttributeVideo):
                return True, int(getattr(attr, "duration", 0) or 0)
    return False, 0

def _target_name_for(lang_key: str, is_video: bool, mime: str | None = None) -> str:
    if is_video:
        # prefer .mp4
        return "flex_ar.mp4" if lang_key == "ar" else "flex_en.mp4"
    # fallback to jpg for images
    return "flex_ar.jpg" if lang_key == "ar" else "flex_en.jpg"

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    media = resolve_media(
        [project_file("flex_ar.mp4"), project_file("flex_ar.jpg"), project_file("flex.jpg")],
        "FLEX_AR_URL",
        DEFAULT_AR_URL,
        cfg_key="ar",
    )
    if media:
        await client.send_file(event.chat_id, file=media, caption="سورس فليكس شغال ✅ استمتع")
    else:
        await event.reply("سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    media = resolve_media(
        [project_file("flex_en.mp4"), project_file("flex_en.jpg")],
        "FLEX_EN_URL",
        DEFAULT_EN_URL,
        cfg_key="en",
    )
    if media:
        await client.send_file(event.chat_id, file=media, caption="Flex source is running ✅ Enjoy")
    else:
        await event.reply("Flex source is running ✅ Enjoy")

# ----------------------
# Commands to set image/video
# ----------------------

# Arabic: ".تعيين صورة فحص (عربي|انجليزي) [url]" (or reply to media: image or video<=10min)
@client.on(events.NewMessage(pattern=r"\.تعيين صورة فحص (عربي|انجليزي)(?:\s+(\S+))?"))
async def set_check_media_ar(event):
    lang = event.pattern_match.group(1)
    maybe_url = event.pattern_match.group(2) or ""
    key = "ar" if lang == "عربي" else "en"

    # URL path: accept as-is (image or video). Note: cannot validate duration for remote URLs.
    if maybe_url:
        CFG[key] = maybe_url.strip()
        _save_cfg(CFG)
        await event.reply(f"✓ تم تعيين وسائط الفحص ({'العربية' if key=='ar' else 'الإنجليزية'}) إلى: {CFG[key]}")
        return

    # Reply path: validate and save
    if event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            is_video, duration = _is_video_message(reply_msg)
            if is_video and duration > MAX_VIDEO_SECONDS:
                await event.reply("⚠️ الفيديو أطول من 10 دقائق. يرجى اختيار فيديو مدة 10 دقائق أو أقل.")
                return
            target_name = _target_name_for(key, is_video)
            target_path = project_file(target_name)
            await client.download_media(reply_msg, file=target_path)
            CFG[key] = target_path
            _save_cfg(CFG)
            await event.reply(f"✓ تم حفظ {'الفيديو' if is_video else 'الصورة'} ({'العربية' if key=='ar' else 'الإنجليزية'}) في: {target_name}")
            return
        except Exception as e:
            await event.reply(f"تعذر حفظ الوسائط: {e}")
            return

    await event.reply("أرسل الأمر مع رابط مباشر لصورة/فيديو أو قم بالرد على صورة/فيديو ثم استخدم الأمر.\nمثال: `.تعيين صورة فحص عربي https://...` أو بالرد ثم: `.تعيين صورة فحص عربي`")

# English: ".set_check_image (ar|en) [url]" (or reply to image/video<=10min)
@client.on(events.NewMessage(pattern=r"\.set_check_image (ar|en)(?:\s+(\S+))?"))
async def set_check_media_en(event):
    lang = event.pattern_match.group(1)
    maybe_url = event.pattern_match.group(2) or ""
    key = "ar" if lang.lower() == "ar" else "en"

    if maybe_url:
        CFG[key] = maybe_url.strip()
        _save_cfg(CFG)
        await event.reply(f"✓ Set check media ({key}) to: {CFG[key]}")
        return

    if event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            is_video, duration = _is_video_message(reply_msg)
            if is_video and duration > MAX_VIDEO_SECONDS:
                await event.reply("⚠️ Video is longer than 10 minutes. Please pick a video ≤ 10 minutes.")
                return
            target_name = _target_name_for(key, is_video)
            target_path = project_file(target_name)
            await client.download_media(reply_msg, file=target_path)
            CFG[key] = target_path
            _save_cfg(CFG)
            await event.reply(f"✓ Saved {'video' if is_video else 'image'} ({key}) to: {target_name}")
            return
        except Exception as e:
            await event.reply(f"Failed to save media: {e}")
            return

    await event.reply("Provide a direct image/video URL or reply to an image/video ≤ 10 minutes, then run the command.\nExample: `.set_check_image ar https://...` or reply then: `.set_check_image ar`")

# ----------------------
# Commands to clear media
# ----------------------

# Arabic clear: ".مسح صورة فحص (عربي|انجليزي)"
@client.on(events.NewMessage(pattern=r"\.مسح صورة فحص (عربي|انجليزي)"))
async def clear_check_media_ar(event):
    lang = event.pattern_match.group(1)
    key = "ar" if lang == "عربي" else "en"
    CFG[key] = ""
    _save_cfg(CFG)
    await event.reply(f"✓ تم مسح وسائط الفحص ({'العربية' if key=='ar' else 'الإنجليزية'}) والرجوع للوضع الافتراضي.")

# English clear: ".clear_check_image (ar|en)"
@client.on(events.NewMessage(pattern=r"\.clear_check_image (ar|en)"))
async def clear_check_media_en(event):
    lang = event.pattern_match.group(1).lower()
    key = "ar" if lang == "ar" else "en"
    CFG[key] = ""
    _save_cfg(CFG)
    await event.reply(f"✓ Cleared check media for ({key}); back to default behavior.")