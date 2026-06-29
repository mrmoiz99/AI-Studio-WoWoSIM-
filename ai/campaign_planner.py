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


def fallback_campaign_plan(topic: str, research: Dict, platform: str = "Instagram") -> Dict:
    lower = f"{topic} {research.get('travel_angle','')}".lower()
    if any(k in lower for k in ["discount", "sale", "offer", "%"]):
        campaign_type = "Discount Offer"
        template = "Discount Offer"
        tone = "clear, urgent, conversion-focused"
    elif any(k in lower for k in ["fifa", "football", "world cup", "match", "stadium"]):
        campaign_type = "Event Travel"
        template = "FIFA / Event Travel"
        tone = "energetic, global, social"
    elif any(k in lower for k in ["airport", "flight", "airline"]):
        campaign_type = "Airport Tip"
        template = "Travel Tip"
        tone = "useful, calm, practical"
    else:
        campaign_type = "Destination Highlight"
        template = "Destination Highlight"
        tone = "premium, modern, inspirational"

    return {
        "campaign_type": campaign_type,
        "platform": platform,
        "template": template,
        "goal": "drive awareness and clicks for WoWoSIM eSIM plans",
        "tone": tone,
        "headline_direction": "short benefit-led headline with travel confidence",
        "visual_strategy": "premium travel background with clear negative space and app-added WoWoSIM branding",
        "cta": research.get("recommended_cta") or "Explore WoWoSIM eSIM plans",
    }


def plan_campaign(topic: str, research: Dict, platform: str = "Instagram", model: str | None = None) -> Dict:
    model = model or get_setting("campaign_planner_model", get_setting("social_posts_model", "llama3.1:latest"))
    prompt = f"""
You are a campaign planner for WoWoSIM, a travel eSIM brand.

Topic:
{topic}

Research brief:
{json.dumps(research, ensure_ascii=False)}

Platform:
{platform}

Return ONLY valid JSON with these exact keys:
{{
  "campaign_type": "Destination Highlight, Travel Tip, Airport Tip, Event Travel, Discount Offer, or Breaking Trend",
  "platform": "platform name",
  "template": "Destination Highlight, Travel Tip, Breaking Trend, FIFA / Event Travel, or Discount Offer",
  "goal": "campaign goal",
  "tone": "tone of voice",
  "headline_direction": "what the final headline should focus on",
  "visual_strategy": "what the background image should support",
  "cta": "short CTA"
}}
"""
    try:
        raw = call_ollama(prompt, model=model, timeout=160)
        data = _json_from_text(raw)
        base = fallback_campaign_plan(topic, research, platform)
        base.update({k: str(v) for k, v in data.items() if v})
        if base.get("template") not in {"Destination Highlight", "Travel Tip", "Breaking Trend", "FIFA / Event Travel", "Discount Offer"}:
            base["template"] = fallback_campaign_plan(topic, research, platform)["template"]
        return base
    except OllamaError:
        return fallback_campaign_plan(topic, research, platform)
