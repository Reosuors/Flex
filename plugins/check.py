import os
import json
from telethon import events
from core.client import client

# Default remote URLs (can be overridden by env vars)
DEFAULT_AR_URL = "https://files.catbox.moe/fcqmhx.jpeg"
DEFAULT_EN_URL = "https://files.catbox.moe/sdzlav.jpeg"

def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def project_file(*parts: str) -> str:
    return os.path.abspath(os.path.join(project_root(), *parts))

# Persistent config for custom images
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

def resolve_image(candidates: list[str], env_var: str, default_url: str | None = None, cfg_key: str | None = None) -> str | None:
    """
    Priority:
    1) Explicitly saved path/url in config (CFG[cfg_key]) if provided.
    2) First existing local file from candidates.
    3) URL from env var.
    4) Default URL.
    """
    if cfg_key:
        cfg_val = (CFG.get(cfg_key) or "").strip()
        if cfg_val:
            # if it's a local path and exists, use it; if it's a URL, use it directly
            if (cfg_val.startswith("http://") or cfg_val.startswith("https://")) or os.path.exists(cfg_val):
                return cfg_val
    for p in candidates:
        if p and os.path.exists(p):
            return p
    url = os.environ.get(env_var) or default_url
    if url:
        return url
    return None

# Simple health-check commands: ".فحص" and ".check"
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source_ar(event):
    img = resolve_image(
        [project_file("flex_ar.jpg"), project_file("flex.jpg")],
        "FLEX_AR_URL",
        DEFAULT_AR_URL,
        cfg_key="ar",
    )
    if img:
        await client.send_file(event.chat_id, file=img, caption="سورس فليكس شغال ✅ استمتع")
    else:
        await event.reply("سورس فليكس شغال ✅ استمتع")

@client.on(events.NewMessage(pattern=r"\.check"))
async def check_source_en(event):
    img = resolve_image(
        [project_file("flex_en.jpg")],
        "FLEX_EN_URL",
        DEFAULT_EN_URL,
        cfg_key="en",
    )
    if img:
        await client.send_file(event.chat_id, file=img, caption="Flex source is running ✅ Enjoy")
    else:
        await event.reply("Flex source is running ✅ Enjoy")

# ----------------------
# Commands to set images
# ----------------------

# Arabic: ".تعيين صورة فحص (عربي|انجليزي) [url]" (or reply to media)
@client.on(events.NewMessage(pattern=r"\.تعيين صورة فحص (عربي|انجليزي)(?:\s+(\S+))?"))
async def set_check_image_ar(event):
    lang = event.pattern_match.group(1)
    maybe_url = event.pattern_match.group(2) or ""
    key = "ar" if lang == "عربي" else "en"
    saved = False

    # If user provided a URL directly
    if maybe_url:
        CFG[key] = maybe_url.strip()
        _save_cfg(CFG)
        saved = True
        await event.reply(f"✓ تم تعيين صورة فحص ({'العربية' if key=='ar' else 'الإنجليزية'}) إلى: {CFG[key]}")
        return

    # Else try to use replied media
    if event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            target_name = "flex_ar.jpg" if key == "ar" else "flex_en.jpg"
            target_path = project_file(target_name)
            await client.download_media(reply_msg, file=target_path)
            CFG[key] = target_path
            _save_cfg(CFG)
            saved = True
            await event.reply(f"✓ تم حفظ الصورة ({'العربية' if key=='ar' else 'الإنجليزية'}) في: {target_name}")
            return
        except Exception as e:
            await event.reply(f"تعذر حفظ الصورة: {e}")

    if not saved:
        await event.reply("أرسل الأمر مع رابط الصورة أو قم بالرد على الصورة ثم استخدم الأمر.\nمثال: `.تعيين صورة فحص عربي https://...` أو بالرد على صورة ثم: `.تعيين صورة فحص عربي`")

# English: ".set_check_image (ar|en) [url]" (or reply to media)
@client.on(events.NewMessage(pattern=r"\.set_check_image (ar|en)(?:\s+(\S+))?"))
async def set_check_image_en(event):
    lang = event.pattern_match.group(1)
    maybe_url = event.pattern_match.group(2) or ""
    key = "ar" if lang.lower() == "ar" else "en"
    saved = False

    if maybe_url:
        CFG[key] = maybe_url.strip()
        _save_cfg(CFG)
        saved = True
        await event.reply(f"✓ Set check image ({key}) to: {CFG[key]}")
        return

    if event.is_reply:
        try:
            reply_msg = await event.get_reply_message()
            target_name = "flex_ar.jpg" if key == "ar" else "flex_en.jpg"
            target_path = project_file(target_name)
            await client.download_media(reply_msg, file=target_path)
            CFG[key] = target_path
            _save_cfg(CFG)
            saved = True
            await event.reply(f"✓ Saved {key} image to: {target_name}")
            return
        except Exception as e:
            await event.reply(f"Failed to save image: {e}")

    if not saved:
        await event.reply("Provide a direct image URL or reply to an image, then run the command.\nExample: `.set_check_image ar https://...` or reply to an image then: `.set_check_image ar`")