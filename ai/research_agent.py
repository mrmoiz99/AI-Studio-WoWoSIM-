import json
import re
from typing import Dict

from ai.ollama import call_ollama, OllamaError
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


def fallback_research(topic: str, caption: str = "") -> Dict:
    text = f"{topic} {caption}".lower()
    destination = "a premium international travel destination"
    if any(k in text for k in ["italy", "rome", "milan", "amalfi", "venice", "vernazza", "florence"]):
        destination = "Italy, with warm coastal or city travel scenery"
    elif any(k in text for k in ["japan", "tokyo", "osaka", "kyoto"]):
        destination = "Japan, with modern city and cultural travel scenery"
    elif any(k in text for k in ["fifa", "football", "world cup", "stadium"]):
        destination = "a football travel destination with stadium atmosphere"
    elif any(k in text for k in ["airport", "flight", "airline"]):
        destination = "a premium airport travel environment"
    elif any(k in text for k in ["summer", "beach", "holiday", "vacation"]):
        destination = "a sunny vacation destination with beach or city escape feeling"

    return {
        "topic_summary": f"{topic} can be used as a travel connectivity angle for WoWoSIM.",
        "travel_angle": "Use the trend to show how travelers need instant mobile data for maps, rides, sharing updates, bookings, and staying connected abroad.",
        "destination_context": destination,
        "audience": "young and mid-age travelers, digital-first tourists, business travelers, and event travelers",
        "brand_connection": "WoWoSIM helps travelers avoid roaming stress with instant eSIM data, hotspot support, and simple activation.",
        "recommended_cta": "Explore WoWoSIM eSIM plans",
        "risk_notes": "Avoid sensitive or tragic framing. Keep the angle positive, practical, and travel-focused.",
    }


def research_topic(topic: str, caption: str = "", model: str | None = None) -> Dict:
    """Create a compact marketing research brief for the trend/topic.

    Uses Ollama when available, but always falls back to deterministic guidance.
    """
    model = model or get_setting("research_model", get_setting("social_posts_model", "llama3.1:latest"))
    prompt = f"""
You are a travel marketing research agent for WoWoSIM, a travel eSIM brand.

Topic or trend:
{topic}

Caption context:
{caption[:1000]}

Return ONLY valid JSON with these exact keys:
{{
  "topic_summary": "one sentence explaining the trend in simple language",
  "travel_angle": "how this can connect to travel or connectivity",
  "destination_context": "specific destination/location/scene suggestion",
  "audience": "specific audience",
  "brand_connection": "natural connection to WoWoSIM eSIM benefits",
  "recommended_cta": "short CTA",
  "risk_notes": "anything to avoid"
}}

Rules:
- If the topic is not directly travel-related, find a natural travel angle only if it makes sense.
- Avoid exploiting disasters, deaths, war, medical emergencies, or tragedies.
- Keep it practical and brand-safe.
"""
    try:
        raw = call_ollama(prompt, model=model, timeout=160)
        data = _json_from_text(raw)
        base = fallback_research(topic, caption)
        base.update({k: str(v) for k, v in data.items() if v})
        return base
    except OllamaError:
        return fallback_research(topic, caption)
