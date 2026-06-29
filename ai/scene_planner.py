import json
import re
from typing import Dict

from ai.ollama import call_ollama, OllamaError
from ai.negative_prompts import get_negative_prompt
from database.database import get_setting


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


def fallback_scene_plan(topic: str, research: Dict, campaign: Dict) -> Dict:
    destination = research.get("destination_context") or "premium international travel destination"
    campaign_type = campaign.get("campaign_type", "Destination Highlight")
    if "Airport" in campaign_type:
        subject = "a modern traveler holding a smartphone near a bright airport window, luggage nearby"
        background = "premium airport terminal with natural light and uncluttered architecture"
        negative_space = "upper-left and center-left clear space"
        crop_anchor = "center"
    elif "Event" in campaign_type:
        subject = "international fans using a smartphone before a major football match"
        background = "stadium exterior or travel city atmosphere with clean sky and flags as subtle color"
        negative_space = "upper third open area"
        crop_anchor = "center"
    else:
        subject = "a traveler using a smartphone while exploring the destination"
        background = destination
        negative_space = "top-left 40 percent of the frame kept simple and uncluttered"
        crop_anchor = "center"
    return {
        "subject": subject,
        "background": background,
        "phone_direction": "smartphone can appear, but the screen must be blank, abstract, or map-like with no readable text",
        "composition": "rule of thirds, subject in lower-right or lower-third, clean open space for app-added headline",
        "negative_space": negative_space,
        "lighting": "golden hour or bright natural commercial light, crisp detail, no motion blur",
        "camera": "realistic 35mm editorial travel photography, premium ad campaign look, sharp focus, high dynamic range",
        "color_notes": "subtle orange #FF5F00 and white accents through clothing, sunlight, luggage tag, or abstract phone glow only",
        "crop_anchor": crop_anchor,
        "negative_prompt": get_negative_prompt(),
    }


def create_scene_plan(topic: str, research: Dict, campaign: Dict, model: str | None = None) -> Dict:
    model = model or get_setting("scene_planner_model", get_setting("image_prompt_model", get_setting("social_posts_model", "llama3.1:latest")))
    prompt = f"""
You are a scene planner for premium travel advertisement photography.

Topic:
{topic}

Research brief:
{json.dumps(research, ensure_ascii=False)}

Campaign plan:
{json.dumps(campaign, ensure_ascii=False)}

The app will add all text/logo/CTA later. You only plan the BACKGROUND PHOTO.

Return ONLY valid JSON with these exact keys:
{{
  "subject": "specific person/object/action in the scene",
  "background": "specific location/environment",
  "phone_direction": "how the smartphone appears if included",
  "composition": "subject placement and framing",
  "negative_space": "where clear empty space should be left for text overlay",
  "lighting": "lighting direction and quality",
  "camera": "camera/lens/style",
  "color_notes": "natural orange #FF5F00 and white accents only",
  "crop_anchor": "center, top, bottom, left, or right",
  "negative_prompt": "things to avoid"
}}

Rules:
- No text, logos, letters, brand names, or UI words in the image.
- Keep the scene simple and clean.
- Make it feel like premium travel photography, not clipart.
"""
    try:
        raw = call_ollama(prompt, model=model, timeout=170)
        data = _json_from_text(raw)
        base = fallback_scene_plan(topic, research, campaign)
        base.update({k: str(v) for k, v in data.items() if v})
        if base.get("crop_anchor") not in {"center", "top", "bottom", "left", "right"}:
            base["crop_anchor"] = "center"
        base["negative_prompt"] = get_negative_prompt(base.get("negative_prompt", ""))
        return base
    except OllamaError:
        return fallback_scene_plan(topic, research, campaign)
