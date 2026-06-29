import json
import re
from typing import Dict, List

from ai.ollama import call_ollama, OllamaError
from database.database import get_setting

DEFAULT_BRIEF = {
    "campaign_angle": "Travel connectivity",
    "audience": "international travelers",
    "emotion": "confidence, freedom, and premium travel ease",
    "scene": "a realistic traveler using a smartphone in a beautiful destination with clear negative space for text",
    "composition": "premium editorial travel photography, subject in lower third, clean sky or soft background in upper area, no clutter",
    "lighting": "crisp golden hour or bright natural commercial lighting with clear details",
    "camera": "realistic high-resolution 35mm commercial photography, sharp focus, professional depth of field",
    "brand_fit": "subtle orange #FF5F00 and white accents may appear naturally through clothing, luggage, sunset, or phone glow",
    "text_space": "top-left or upper-third negative space for app-added headline",
    "crop_anchor": "center",
    "negative_prompt": "no text, no logo, no watermark, no random letters, no distorted hands, no clutter, no cartoon, no painting, no blurry image",
}


def _json_from_text(text: str) -> Dict:
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"\{.*\}", text or "", re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return {}


def create_visual_brief(topic: str, caption: str = "", platform: str = "Instagram", model: str | None = None) -> Dict:
    model = model or get_setting("image_prompt_model", get_setting("social_posts_model", "llama3.1:latest"))
    prompt = f"""
You are the Creative Director for WoWoSIM, a travel eSIM brand.

Your job is NOT to write a caption. Your job is to brief a photographer/image model for a clean background image. The app will add all WoWoSIM logo, headline, CTA, pricing, and text later.

Topic or trend:
{topic}

Caption context:
{caption[:900]}

Platform:
{platform}

Return ONLY valid JSON with these exact keys:
{{
  "campaign_angle": "short marketing angle",
  "audience": "specific audience",
  "emotion": "desired feeling",
  "scene": "specific photo scene with destination, person/object, smartphone if useful",
  "composition": "where the subject sits, where empty space exists, what must stay uncluttered",
  "lighting": "lighting style that creates crisp professional details",
  "camera": "realistic camera/lens/style direction",
  "brand_fit": "how orange #FF5F00 and white can appear naturally without logos/text",
  "text_space": "where the final design should have empty space for headline",
  "crop_anchor": "center, top, bottom, left, or right",
  "negative_prompt": "things to avoid"
}}

Rules:
- Choose one specific visual idea, not generic travel words.
- Prefer realistic premium travel photography.
- Create empty space for the design layer.
- Do not ask for text, words, logos, UI text, or watermarks inside the AI image.
- Do not mention WoWoSIM logo inside the image.
- Avoid crowded scenes because text will be added later.
"""
    try:
        raw = call_ollama(prompt, model=model, timeout=180)
        brief = _json_from_text(raw)
        if not brief:
            return DEFAULT_BRIEF.copy()
        merged = DEFAULT_BRIEF.copy()
        merged.update({k: str(v) for k, v in brief.items() if v})
        if merged.get("crop_anchor") not in {"center", "top", "bottom", "left", "right"}:
            merged["crop_anchor"] = "center"
        return merged
    except OllamaError:
        return DEFAULT_BRIEF.copy()


def build_production_prompt(brief: Dict, topic: str = "") -> str:
    return f"""
Create a high-resolution, sharp, realistic travel photography background for a premium social media advertisement.

Topic inspiration: {topic}
Campaign angle: {brief.get('campaign_angle')}
Audience: {brief.get('audience')}
Emotion: {brief.get('emotion')}

Scene:
{brief.get('scene')}

Composition:
{brief.get('composition')}
Text safe area:
{brief.get('text_space')}

Lighting:
{brief.get('lighting')}

Camera/style:
{brief.get('camera')}
Use crisp details, clean focus, professional commercial photography, natural color grading, realistic depth, high dynamic range, and no motion blur.

Brand fit:
{brief.get('brand_fit')}

Important:
This is ONLY the background image. Leave clean negative space for the app to add typography and CTA later. Do not generate any text or logo.

Strict negative prompt:
{brief.get('negative_prompt')}, no text, no logo, no watermark, no random letters, no misspelled words, no fake interface text, no messy typography, no deformed hands, no distorted faces, no extra fingers, no clutter, no low resolution, no blurry background, no over-processed image.
""".strip()


def score_image_prompt(prompt: str, brief: Dict, index: int) -> int:
    score = 70
    keywords = ["sharp", "realistic", "premium", "negative space", "lighting", "composition", "clean", "high-resolution"]
    text = (prompt + " " + json.dumps(brief)).lower()
    score += sum(3 for k in keywords if k in text)
    score += (index * 5) % 13
    return min(98, score)


def make_prompt_variations(base_prompt: str, count: int = 4) -> List[str]:
    styles = [
        "Variation A: wide cinematic destination background with large clean negative space in the upper third, crisp and premium.",
        "Variation B: smartphone in the foreground with a sharp destination background, clean composition, no visible text on the screen.",
        "Variation C: authentic traveler lifestyle moment, subject in lower third, simple background, warm commercial lighting.",
        "Variation D: luxury editorial travel style, strong geometry, uncluttered sky or architecture, premium ad photography.",
    ]
    count = max(1, min(count, 4))
    return [f"{base_prompt}\n\n{styles[i]}" for i in range(count)]
