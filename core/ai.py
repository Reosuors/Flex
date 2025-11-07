import asyncio
from typing import Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None

from core.config import GEMINI_API_KEY

_MODEL_NAME = "gemini-1.5-flash"
_model = None
_configured = False


def _ensure_configured():
    global _configured, _model
    if _configured:
        return
    if genai is None or not GEMINI_API_KEY:
        _configured = True
        _model = None
        return
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(_MODEL_NAME)
    except Exception:
        _model = None
    finally:
        _configured = True


async def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.6) -> Optional[str]:
    """
    Generate a short response using Gemini if available; otherwise return None.
    Runs the blocking SDK in a thread to avoid blocking the event loop.
    """
    _ensure_configured()
    if _model is None:
        return None

    def _call():
        # The python SDK for Gemini is synchronous
        resp = _model.generate_content(
            prompt,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
        )
        try:
            return (resp.text or "").strip()
        except Exception:
            # Some SDK versions use candidates
            try:
                return (resp.candidates[0].content.parts[0].text or "").strip()
            except Exception:
                return None

    return await asyncio.to_thread(_call)