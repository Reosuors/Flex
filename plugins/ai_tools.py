import re
from telethon import events
from core.client import client

# Translation and language detection utilities
# Libraries available in requirements: gpytranslate, deep-translator, langdetect
try:
    from gpytranslate import Translator as GPTranslator
except Exception:
    GPTranslator = None

try:
    from deep_translator import GoogleTranslator as DTGoogleTranslator
except Exception:
    DTGoogleTranslator = None

try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
except Exception:
    detect = None

# Common language code mapping (extendable)
LANG_MAP = {
    "ar": "ar",
    "arabic": "ar",
    "عربي": "ar",
    "en": "en",
    "english": "en",
    "انجليزي": "en",
    "fr": "fr",
    "فرنسي": "fr",
    "de": "de",
    "الماني": "de",
    "es": "es",
    "اسباني": "es",
    "tr": "tr",
    "تركي": "tr",
    "fa": "fa",
    "فارسي": "fa",
    "ru": "ru",
    "روسي": "ru",
    "it": "it",
    "ايطالي": "it",
}

ARABIC_STOPWORDS = set("""
في من على إلى و أن إن كان كانت يكون تكون لكن أو ثم حيث كما الذي التي الذين هذا هذه ذلك تلك لأن حتى مع خلال ضد بين لدى عند قبل بعد دون فقط جدا أكثر أقل نفس مثل حول إلى عن إلا إذا ما لن لم لا كل بعض أيًا أي اي نعم لا
""".split())

def normalize_lang(lang: str) -> str:
    key = (lang or "").strip().lower()
    return LANG_MAP.get(key, key)

async def translate_text(text: str, target: str) -> str:
    target = normalize_lang(target)
    # Try gpytranslate first
    if GPTranslator is not None:
        try:
            tr = GPTranslator()
            res = await tr.translate(text, target)
            return res.text
        except Exception:
            pass
    # Fallback to deep-translator Google
    if DTGoogleTranslator is not None:
        try:
            return DTGoogleTranslator(source="auto", target=target).translate(text)
        except Exception:
            pass
    return "تعذر الترجمة الآن. حاول لاحقًا."

def simple_summarize(text: str, max_sentences: int = 3) -> str:
    # Split into sentences (basic Arabic/English punctuation)
    sentences = re.split(r"(?<=[.!؟])\s+", (text or "").strip())
    if len(sentences) <= max_sentences:
        return text
    # Tokenize and score by word frequency excluding stopwords
    words = re.findall(r"\b[\w\u0621-\u064A]+\b", text.lower())
    freq = {}
    for w in words:
        if w in ARABIC_STOPWORDS or len(w) <= 2:
            continue
        freq[w] = freq.get(w, 0) + 1
    scores = []
    for s in sentences:
        sw = re.findall(r"\b[\w\u0621-\u064A]+\b", s.lower())
        score = sum(freq.get(w, 0) for w in sw)
        scores.append((score, s))
    # Pick top sentences keeping original order
    top = sorted(scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    selected = set(s for _, s in top)
    result = [s for s in sentences if s in selected]
    return " ".join(result)

# --- Advanced AI reply (.ذكاء) with OpenAI if available, fallback to simple rules ---
def ai_reply_simple(text: str) -> str:
    t = (text or "").strip().lower()
    if "السلام" in t or "مرحبا" in t or "اهلا" in t or "هلا" in t:
        return "وعليكم السلام! كيف أقدر أساعدك؟"
    if "كيف حالك" in t or "شلونك" in t or "كيفك" in t:
        return "بخير الحمد لله! وأنت؟"
    if "شكرا" in t or "شكرًا" in t or "ثانكس" in t:
        return "العفو! هذا واجبي."
    if "من انت" in t or "مين انت" in t or "من أنت" in t:
        return "أنا مساعد FLEX الذكي—أساعدك بالأوامر والترجمة والملخصات."
    return "حاضر! فهمت سؤالك، لكن كـ'رد ذكي' مختصر: محتاج توضيح أكثر؟"

async def ai_reply_openai(prompt: str) -> str:
    try:
        from core.config import OPENAI_API_KEY
        if not OPENAI_API_KEY:
            return ai_reply_simple(prompt)
        # Use new OpenAI SDK
        try:
            from openai import OpenAI
        except Exception:
            # SDK not installed; fallback
            return ai_reply_simple(prompt)
        client_ai = OpenAI(api_key=OPENAI_API_KEY)
        system_msg = "أنت مساعد عربي لطيف ومختصر، تجيب بإيجاز وبأسلوب محترم، وترد دائمًا باللغة التي سُئلت بها."
        resp = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            max_tokens=150,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return ai_reply_simple(prompt)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ذكاء(?:\s+([\s\S]+))?$"))
async def ai_cmd(event):
    msg = event.pattern_match.group(1)
    if not msg and event.is_reply:
        reply = await event.get_reply_message()
        msg = reply.message or reply.raw_text
    if not msg:
        await event.edit("اكتب: .ذكاء <سؤالك> أو بالرد على رسالة.\nمثال: .ذكاء كيف حالك")
        return
    answer = await ai_reply_openai(msg)
    await event.edit(answer)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ترجم\s+(\S+)(?:\s+([\s\S]+))?$"))
async def translate_cmd(event):
    target = event.pattern_match.group(1)
    inline_text = event.pattern_match.group(2)
    text = inline_text
    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.message or reply.raw_text
    if not text:
        await event.edit("استخدم: .ترجم <لغة> <نص> أو بالرد على رسالة.\nمثال: .ترجم en مرحبًا بك")
        return
    translated = await translate_text(text, target)
    await event.edit(f"الترجمة ({normalize_lang(target)}):\n{translated}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.كشف_لغة(?:\s+([\s\S]+))?$"))
async def detect_lang_cmd(event):
    text = event.pattern_match.group(1)
    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.message or reply.raw_text
    if not text:
        await event.edit("استخدم: .كشف_لغة <نص> أو بالرد على رسالة.")
        return
    if detect is None:
        await event.edit("ميزة كشف اللغة غير متاحة الآن.")
        return
    try:
        code = detect(text)
        await event.edit(f"اللغة المكتشفة: {code}")
    except Exception as e:
        await event.edit(f"تعذر كشف اللغة: {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.تلخيص(?:\s+(\d+))?$"))
async def summarize_cmd(event):
    n_raw = event.pattern_match.group(1)
    max_sentences = int(n_raw) if n_raw else 3
    text = None
    if event.is_reply:
        reply = await event.get_reply_message()
        text = reply.message or reply.raw_text
    if not text:
        await event.edit("استخدم: .تلخيص [عدد_الجمل] بالرد على نص طويل.")
        return
    summary = simple_summarize(text, max_sentences=max_sentences)
    await event.edit(f"ملخص ({max_sentences}):\n{summary}")