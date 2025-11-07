import asyncio
from typing import Optional

try:
    from groq import Groq
except Exception:
    Groq = None  # type: ignore

from core.config import GROQ_API_KEY

# Default Groq model
_GROQ_MODEL = "llama-3.1-70b-versatile"

_groq_client = None
_configured = False


def _ensure_configured():
    global _configured, _groq_client
    if _configured:
        return
    if GROQ_API_KEY and Groq is not None:
        try:
            _groq_client = Groq(api_key=GROQ_API_KEY)
        except Exception:
            _groq_client = None
    _configured = True


async def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.6) -> Optional[str]:
    """
    Generate a short response using Groq (Llama). Returns None if not configured.
    """
    _ensure_configured()
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