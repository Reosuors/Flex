import asyncio
from typing import Optional

# Optional providers
try:
    import google.generativeai as genai
except Exception:
    genai = None

try:
    from groq import Groq
except Exception:
    Groq = None  # type: ignore

from core.config import GEMINI_API_KEY, GROQ_API_KEY

# Default models
_GEMINI_MODEL = "gemini-1.5-flash"
_GROQ_MODEL = "llama-3.1-70b-versatile"

# Provider state
_gemini_model = None
_groq_client = None
_configured = False


def _ensure_configured():
    global _configured, _gemini_model, _groq_client
    if _configured:
        return

    # Configure Groq first (preferred if key present)
    if GROQ_API_KEY and Groq is not None:
        try:
            _groq_client = Groq(api_key=GROQ_API_KEY)
        except Exception:
            _groq_client = None

    # Configure Gemini as fallback
    if GEMINI_API_KEY and genai is not None:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            _gemini_model = genai.GenerativeModel(_GEMINI_MODEL)
        except Exception:
            _gemini_model = None

    _configured = True


async def _call_groq(prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
    if _groq_client is None:
        return None

    def _call():
        try:
            resp = _groq_client.chat.completions.create(
                model=_GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "أجب بإيجاز وبوضوح وبنفس لغة المستخدم."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception:
            return None

    return await asyncio.to_thread(_call)


async def _call_gemini(prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
    if _gemini_model is None:
        return None

    def _call():
        try:
            resp = _gemini_model.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
            )
            try:
                return (resp.text or "").strip()
            except Exception:
                try:
                    return (resp.candidates[0].content.parts[0].text or "").strip()  # type: ignore
                except Exception:
                    return None
        except Exception:
            return None

    return await asyncio.to_thread(_call)


async def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.6) -> Optional[str]:
    """
    Generate a short response using Groq if configured, otherwise Gemini if available.
    Returns None if no provider is configured.
    """
    _ensure_configured()

    # Prefer Groq
    text = await _call_groq(prompt, max_tokens=max_tokens, temperature=temperature)
    if text:
        return text

    # Fallback to Gemini
    text = await _call_gemini(prompt, max_tokens=max_tokens, temperature=temperature)
    if text:
        return text

    return None