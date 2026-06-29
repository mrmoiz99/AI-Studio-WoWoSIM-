import base64
from io import BytesIO

from PIL import Image

from config import ENV_GEMINI_API_KEY
from database.database import get_setting


def _get_api_key() -> str:
    """Load Gemini key from the app Settings first, then .env/environment."""
    api_key = (get_setting("gemini_api_key", "") or "").strip()
    if not api_key:
        api_key = (ENV_GEMINI_API_KEY or "").strip()
    if not api_key:
        raise RuntimeError(
            "Gemini API key missing. Open Settings → API Keys, paste your Gemini API key, and click Save API Keys."
        )
    return api_key


def _save_bytes_to_image(data: bytes) -> Image.Image:
    return Image.open(BytesIO(data)).convert("RGB")


def _extract_image_from_response(response) -> Image.Image:
    """Handle common google-genai image response shapes."""
    candidates = getattr(response, "candidates", []) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", []) if content else []
        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                data = inline.data
                if isinstance(data, str):
                    data = base64.b64decode(data)
                return _save_bytes_to_image(data)

    # Some SDK versions expose a direct output list.
    outputs = getattr(response, "outputs", None) or getattr(response, "output", None) or []
    if not isinstance(outputs, list):
        outputs = [outputs]
    for item in outputs:
        for attr in ("image", "data", "bytes"):
            value = getattr(item, attr, None)
            if isinstance(value, bytes):
                return _save_bytes_to_image(value)
            if isinstance(value, str):
                try:
                    return _save_bytes_to_image(base64.b64decode(value))
                except Exception:
                    pass

    raise RuntimeError(
        "Gemini did not return an image. Check that your selected Gemini image model supports image output and that your API key has access."
    )


def generate(prompt: str, width: int = 1080, height: int = 1350, model: str = "gemini-3.1-flash-image") -> Image.Image:
    """Gemini image generation provider using the API key saved in Settings."""
    api_key = _get_api_key()

    try:
        from google import genai
        from google.genai import types
    except Exception as exc:
        raise RuntimeError("Install Gemini SDK first: pip install google-genai") from exc

    client = genai.Client(api_key=api_key)
    aspect_ratio = "4:5" if height > width else "1:1" if height == width else "16:9"

    # Gemini image models generally respond better to concise production prompts.
    final_prompt = f"""
Create a sharp realistic travel background image only.
Aspect ratio: {aspect_ratio}.
{prompt}
No text, no logo, no watermark, no letters, no poster layout.
Leave clean negative space for branding overlay.
""".strip()

    # Preferred generate_content path for image-capable Gemini models.
    try:
        response = client.models.generate_content(
            model=model,
            contents=final_prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
    except TypeError:
        response = client.models.generate_content(model=model, contents=final_prompt)

    return _extract_image_from_response(response)
