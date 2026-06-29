import random
import re
import urllib.parse
from io import BytesIO

import requests
from PIL import Image


def _clean_prompt(prompt: str, max_chars: int = 850) -> str:
    """Keep Pollinations prompts short and URL-safe.

    Pollinations uses a path-based URL. Very long prompts, markdown, hashtags,
    slashes, and special characters can cause 404/500 errors. The Creative
    Director can still make a detailed brief, but this provider needs a compact
    production prompt.
    """
    text = str(prompt or "")
    text = re.sub(r"\*\*|__|```|#+", "", text)
    text = text.replace("#FF5F00", "orange")
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9,.()\-:; ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Keep the strongest visual rules and remove verbose internal sections.
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0]

    negative = " no text, no logo, no watermark, no letters, no blurry image"
    base = text + negative
    return base[: max_chars + len(negative)]


def generate(prompt: str, width: int = 1080, height: int = 1350, model: str = "turbo") -> Image.Image:
    seed = random.randint(10000, 999999)

    # Pollinations is much more stable at these sizes. Higher quality is handled
    # later by local crop/sharpen/upscale in the background processor.
    width = min(int(width or 1080), 1280)
    height = min(int(height or 1350), 1280)

    final_prompt = _clean_prompt(prompt)
    encoded_prompt = urllib.parse.quote(final_prompt, safe="")

    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    params = {
        "width": width,
        "height": height,
        "model": model or "turbo",
        "seed": seed,
        "nologo": "true",
    }

    response = requests.get(url, params=params, timeout=240)
    if response.status_code == 404:
        raise RuntimeError(
            "Pollinations returned 404. The prompt/model/size was rejected. "
            "Try Gemini as the image provider, or use Pollinations with model='turbo' and size <=1280."
        )
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGB")
