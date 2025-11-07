import re
import asyncio
from typing import List, Tuple, Optional

from telethon import events, Button
from core.bot_client import bot

# Optional libraries used if available
try:
    from gpytranslate import Translator as GPTranslator  # async
except Exception:
    GPTranslator = None

try:
    from deep_translator import GoogleTranslator as DTGoogleTranslator  # sync
except Exception:
    DTGoogleTranslator = None

# HTTP client for utilities
try:
    import aiohttp
except Exception:
    aiohttp = None

# Optional OpenAI
try:
    from core.config import OPENAI_API_KEY
    if OPENAI_API_KEY:
        from openai import OpenAI
    else:
        OpenAI = None
except Exception:
    OPENAI_API_KEY = None
    OpenAI = None


AR = "AR"
EN = "EN"


def _ai_reply_simple(text: str, lang: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["السلام", "مرحبا", "اهلا", "هلا"]):
        return "وعليكم السلام! كيف أساعدك؟" if lang == AR else "Wa Alaikum Assalam! How can I help?"
    if any(w in t for w in ["كيف حالك", "شلونك", "كيفك", "how are you"]):
        return "بخير الحمد لله! وأنت؟" if lang == AR else "I’m good, thanks! And you?"
    if any(w in t for w in ["شكرا", "شكر", "thanks", "thank you"]):
        return "على الرحب والسعة!" if lang == AR else "You’re welcome!"
    return "حاضر. هل يمكنك التوضيح أكثر؟" if lang == AR else "Got it. Could you clarify a bit more?"


async def _ai_reply(prompt: str, lang: str) -> str:
    if OpenAI is None or not OPENAI_API_KEY:
        return _ai_reply_simple(prompt, lang)
    try:
        client_ai = OpenAI(api_key=OPENAI_API_KEY)
        system_msg = "أجب باختصار وبنفس لغة المستخدم." if lang == AR else "Answer briefly in the user's language."
        resp = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=180,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return _ai_reply_simple(prompt, lang)


def _simple_summarize(text: str, max_sentences: int = 3) -> str:
    sentences = re.split(r"(?<=[.!؟])\s+", (text or "").strip())
    if len(sentences) <= max_sentences:
        return text
    words = re.findall(r"\b[\w\u0621-\u064A]+\b", text.lower())
    stop_ar = set("في من على إلى و أن إن كان كانت يكون تكون لكن أو ثم حيث كما الذي التي الذين هذا هذه ذلك تلك لأن حتى مع خلال ضد بين لدى عند قبل بعد دون فقط جدا أكثر أقل نفس مثل حول إلى عن إلا إذا ما لن لم لا كل بعض أيًا أي اي".split())
    freq = {}
    for w in words:
        if w in stop_ar or len(w) <= 2:
            continue
        freq[w] = freq.get(w, 0) + 1
    scores = []
    for s in sentences:
        sw = re.findall(r"\b[\w\u0621-\u064A]+\b", s.lower())
        score = sum(freq.get(w, 0) for w in sw)
        scores.append((score, s))
    top = sorted(scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    selected = set(s for _, s in top)
    result = [s for s in sentences if s in selected]
    return " ".join(result)


async def _translate(text: str, target: str) -> str:
    target = (target or "").strip().lower()
    # Try gpytranslate first
    if GPTranslator is not None:
        try:
            tr = GPTranslator()
            res = await tr.translate(text, target)
            return res.text
        except Exception:
            pass
    if DTGoogleTranslator is not None:
        try:
            return DTGoogleTranslator(source="auto", target=target).translate(text)
        except Exception:
            pass
    return "تعذر الترجمة الآن." if target == "ar" else "Translation unavailable now."


async def _shorten(url: str) -> Optional[str]:
    if aiohttp is None:
        return None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://tinyurl.com/api-create.php", params={"url": url}, timeout=10) as resp:
                if resp.status == 200:
                    return (await resp.text()).strip()
    except Exception:
        return None
    return None


async def _fetch_title(url: str) -> Optional[str]:
    if aiohttp is None:
        return None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return None
                html = await resp.text(errors="ignore")
                m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                if m:
                    return re.sub(r"\s+", " ", m.group(1)).strip()
    except Exception:
        return None
    return None


def _detect_lang_from_query(q: str) -> str:
    # default AR if Arabic letters present
    return AR if re.search(r"[\u0600-\u06FF]", q or "") else EN


def _menu_text(lang: str) -> str:
    if lang == AR:
        return (
            "قائمة المساعد (Inline)\n"
            "- ai: س → ذكاء اصطناعي سريع\n"
            "- tr: en مرحبًا → ترجمة\n"
            "- sum:3 نص طويل → تلخيص\n"
            "- short: https://.. → تقصير رابط\n"
            "- url: https://.. → عنوان الصفحة\n"
            "أمثلة:\n"
            "ai: كيف حالك؟\n"
            "tr: ar hello world\n"
            "sum:2 هذا نص طويل ...\n"
            "short: https://example.com/page\n"
            "url: https://example.com\n"
        )
    return (
        "Assistant Menu (Inline)\n"
        "- ai: q → quick AI\n"
        "- tr: <lang> text → translate\n"
        "- sum:3 long text → summarize\n"
        "- short: https://.. → shorten URL\n"
        "- url: https://.. → fetch page title\n"
        "Examples:\n"
        "ai: how are you?\n"
        "tr: en مرحبًا\n"
        "sum:2 this is a very long text ...\n"
        "short: https://example.com/page\n"
        "url: https://example.com\n"
    )


def _menu_buttons(lang: str):
    if lang == AR:
        return [
            [Button.inline("ذكاء (ai)", data=b"asst:AR:demo:ai"),
             Button.inline("ترجمة (tr)", data=b"asst:AR:demo:tr")],
            [Button.inline("تلخيص (sum)", data=b"asst:AR:demo:sum"),
             Button.inline("روابط (short/url)", data=b"asst:AR:demo:link")],
            [Button.inline("English", data=b"asst:EN:menu")],
        ]
    return [
        [Button.inline("AI (ai)", data=b"asst:EN:demo:ai"),
         Button.inline("Translate (tr)", data=b"asst:EN:demo:tr")],
        [Button.inline("Summarize (sum)", data=b"asst:EN:demo:sum"),
         Button.inline("Links (short/url)", data=b"asst:EN:demo:link")],
        [Button.inline("العربية", data=b"asst:AR:menu")],
    ]


if bot is not None:
    # /start and /help for the assistant bot
    @bot.on(events.NewMessage(pattern=r"^/(start|help)$"))
    async def bot_start(event):
        # Always ask for language explicitly
        text = "اختر لغتك • Choose your language"
        buttons = [
            [Button.inline("عربي", data=b"asst:AR:menu"), Button.inline("English", data=b"asst:EN:menu")]
        ]
        await event.respond(text, buttons=buttons)

    @bot.on(events.CallbackQuery)
    async def asst_callbacks(event):
        data = (event.data or b"").decode(errors="ignore")
        if not data.startswith("asst:"):
            return
        parts = data.split(":")
        if len(parts) < 3:
            await event.answer("Bad data", alert=True)
            return
        lang = parts[1]
        action = parts[2]
        if action == "menu":
            await event.edit(_menu_text(lang), buttons=_menu_buttons(lang))
            await event.answer("OK")
            return
        if action == "demo":
            demo = parts[3] if len(parts) > 3 else ""
            if lang == AR:
                if demo == "ai":
                    await event.answer("مثال: ai: كيف حالك؟", alert=True)
                elif demo == "tr":
                    await event.answer("مثال: tr: en مرحبًا بك", alert=True)
                elif demo == "sum":
                    await event.answer("مثال: sum:2 هذا نص طويل جدًا...", alert=True)
                else:
                    await event.answer("short: https://.. | url: https://..", alert=True)
            else:
                if demo == "ai":
                    await event.answer("Example: ai: how are you?", alert=True)
                elif demo == "tr":
                    await event.answer("Example: tr: ar hello world", alert=True)
                elif demo == "sum":
                    await event.answer("Example: sum:2 this is a very long text...", alert=True)
                else:
                    await event.answer("short: https://.. | url: https://..", alert=True)
            return

    @bot.on(events.InlineQuery)
    async def inline_handler(event):
        q = (event.query or "").strip()
        lang = _detect_lang_from_query(q)

        async def article(title: str, text: str):
            return event.builder.article(title=title, text=text, description=text[:120])

        # Empty query -> show menu hint
        if not q:
            await event.answer([await article("Assistant Menu • FLEX", _menu_text(lang))], cache_time=0)
            return

    # -------------------------
    # Relay (Contact) Bot Logic
    # -------------------------
    # Persist mapping from owner's received bot messages -> original user ids
    import os, json

    RELAY_MAP_FILE = "relay_map.json"
    _RELAY_MAP = None
    _OWNER_ID = None

    def _load_map():
        nonlocal _RELAY_MAP
        if _RELAY_MAP is not None:
            return _RELAY_MAP
        if os.path.exists(RELAY_MAP_FILE) and os.stat(RELAY_MAP_FILE).st_size > 0:
            try:
                with open(RELAY_MAP_FILE, "r", encoding="utf-8") as f:
                    _RELAY_MAP = json.load(f)
            except Exception:
                _RELAY_MAP = {}
        else:
            _RELAY_MAP = {}
        return _RELAY_MAP

    def _save_map():
        if _RELAY_MAP is None:
            return
        try:
            with open(RELAY_MAP_FILE, "w", encoding="utf-8") as f:
                json.dump(_RELAY_MAP, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    async def _get_owner_id():
        nonlocal _OWNER_ID
        if _OWNER_ID:
            return _OWNER_ID
        try:
            # Use the user session to fetch owner's id once
            from core.client import client as user_client
            me = await user_client.get_me()
            _OWNER_ID = me.id
        except Exception:
            _OWNER_ID = None
        return _OWNER_ID

    async def _send_to_owner(src_event):
        """
        Forward a message from any user (not owner) to the owner with metadata and save mapping.
        """
        owner_id = await _get_owner_id()
        if not owner_id:
            return
        from_user = await src_event.get_sender()
        user_id = from_user.id
        if getattr(from_user, "bot", False):
            # ignore other bots
            return

        # Build metadata
        username = ("@" + from_user.username) if getattr(from_user, "username", None) else "—"
        name = (getattr(from_user, "first_name", "") or "") + (" " + (getattr(from_user, "last_name", "") or "")).strip()
        meta = f"رسالة جديدة من المستخدم\nName: {name or '—'}\nID: {user_id}\nUsername: {username}"

        # Relay
        try:
            if src_event.message and src_event.message.media:
                cap = (src_event.raw_text or "")  # include any text
                sent = await bot.send_file(owner_id, src_event.message, caption=(meta + ("\n\n" + cap if cap else "")))
            else:
                text = (src_event.raw_text or "")
                sent = await bot.send_message(owner_id, meta + ("\n\n" + text if text else ""))
        except Exception:
            return

        # Map reply target
        try:
            _map = _load_map()
            _map[str(sent.id)] = user_id
            _save_map()
        except Exception:
            pass

    async def _reply_to_user(owner_event):
        """
        Owner replies to a relayed message: deliver the reply back to original user.
        """
        owner_id = await _get_owner_id()
        if not owner_id or owner_event.sender_id != owner_id:
            return
        if not owner_event.is_reply:
            return
        try:
            reply_msg = await owner_event.get_reply_message()
            original_map = _load_map()
            target_user_id = original_map.get(str(reply_msg.id))
            if not target_user_id:
                # Fallback: try parse ID from metadata text
                m = re.search(r"ID:\s*(\d+)", (reply_msg.raw_text or ""))
                if m:
                    target_user_id = int(m.group(1))
            if not target_user_id:
                return
        except Exception:
            return

        # Send owner's reply to original user
        try:
            if owner_event.message and owner_event.message.media:
                cap = (owner_event.raw_text or "")
                await bot.send_file(target_user_id, owner_event.message, caption=cap)
            else:
                await bot.send_message(target_user_id, (owner_event.raw_text or ""))
        except Exception:
            pass

    # Handle incoming messages for relay
    @bot.on(events.NewMessage(incoming=True))
    async def relay_handler(event):
        # Ignore service/inline messages
        if event.via_bot_id:
            return
        owner_id = await _get_owner_id()
        if not owner_id:
            return

        # If message from owner in bot dialog: treat as potential reply to user
        if event.is_private and event.sender_id == owner_id:
            await _reply_to_user(event)
            return

        # If message from any other user (private) -> relay to owner
        if event.is_private and event.sender_id != owner_id:
            await _send_to_owner(event)
            return

        # Ignore groups/channels for now
        return

        # ai: prompt
        m = re.match(r"^ai:\s*(.+)$", q, flags=re.IGNORECASE)
        if m:
            prompt = m.group(1)
            ans = await _ai_reply(prompt, lang)
            await event.answer([await article("AI • Answer", ans)], cache_time=0)
            return

        # tr: <lang> <text>
        m = re.match(r"^tr:\s*([A-Za-z\u0600-\u06FF]+)\s+(.+)$", q, flags=re.IGNORECASE)
        if m:
            target, text = m.group(1), m.group(2)
            translated = await _translate(text, target)
            await event.answer([await article(f"Translate → {target}", translated)], cache_time=0)
            return

        # sum: N text
        m = re.match(r"^sum:\s*(\d{1,2})\s+(.+)$", q, flags=re.IGNORECASE)
        if m:
            n = int(m.group(1))
            text = m.group(2)
            n = max(1, min(n, 10))
            summary = _simple_summarize(text, n)
            await event.answer([await article(f"Summary ({n})", summary)], cache_time=0)
            return

        # short: URL
        m = re.match(r"^short:\s*(https?://\S+)$", q, flags=re.IGNORECASE)
        if m:
            url = m.group(1)
            short = await _shorten(url)
            if not short:
                short = "تعذر تقصير الرابط حالياً." if lang == AR else "Could not shorten URL now."
            await event.answer([await article("Short URL", short)], cache_time=0)
            return

        # url: URL -> title
        m = re.match(r"^url:\s*(https?://\S+)$", q, flags=re.IGNORECASE)
        if m:
            url = m.group(1)
            title = await _fetch_title(url)
            title = title or (("لم يُعثر على عنوان." if lang == AR else "No title found.") + f"\n{url}")
            await event.answer([await article("Page Title", title)], cache_time=0)
            return

        # Fallback: show menu hint and brief AI try
        if len(q) >= 4:
            ans = await _ai_reply(q, lang)
            await event.answer([await article("AI • Quick", ans)], cache_time=0)
        else:
            await event.answer([await article("Assistant Menu • FLEX", _menu_text(lang))], cache_time=0)