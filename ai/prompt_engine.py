import re
from typing import Dict

from ai.negative_prompts import get_negative_prompt
from ai.prompt_library import load_template


def compact_prompt(text: str, max_chars: int = 1500) -> str:
    """Keep prompts provider-safe, especially for URL-based free APIs."""
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = text.replace("#", "")  # Pollinations URL paths can be sensitive to hashes.
    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "."
    return text


def build_image_prompt_from_plan(topic: str, research: Dict, campaign: Dict, scene: Dict, variation_note: str = "") -> str:
    template_text = load_template(campaign.get("template", "Destination Highlight"))
    prompt = f"""
{template_text}

Topic inspiration: {topic}
Campaign type: {campaign.get('campaign_type')}
Marketing goal: {campaign.get('goal')}
Audience: {research.get('audience')}
Travel angle: {research.get('travel_angle')}

Subject: {scene.get('subject')}
Background/location: {scene.get('background')}
Smartphone direction: {scene.get('phone_direction')}
Composition: {scene.get('composition')}
Negative space: {scene.get('negative_space')}
Lighting: {scene.get('lighting')}
Camera/style: {scene.get('camera')}
Color notes: {scene.get('color_notes')}

Strict rules: generate only the background photo, no ad layout, no readable text, no logo, no brand name, no watermark. The application will add all WoWoSIM typography and CTA later.
Negative prompt: {get_negative_prompt(scene.get('negative_prompt', ''))}
{variation_note}
""".strip()
    return compact_prompt(prompt, max_chars=1600)


def make_prompt_variations_from_plan(topic: str, research: Dict, campaign: Dict, scene: Dict, count: int = 4):
    notes = [
        "Variation A: wide clean composition with strong open space for headline overlay and crisp destination detail.",
        "Variation B: smartphone foreground detail with destination atmosphere behind it, screen blank or abstract, no words.",
        "Variation C: authentic traveler lifestyle moment, subject in lower third, warm natural light, premium feel.",
        "Variation D: luxury editorial travel scene with simple geometry, clean sky or architecture, high clarity.",
    ]
    count = max(1, min(int(count or 1), 4))
    return [build_image_prompt_from_plan(topic, research, campaign, scene, notes[i]) for i in range(count)]


def optimize_background_prompt(prompt: str) -> str:
    return compact_prompt(f"""
{prompt}
Realistic high quality commercial travel photography. Sharp focus. Clean negative space. Premium modern social media campaign look. No text, no logo, no watermark, no letters.
""", max_chars=1600)


def optimize_image_prompt(prompt: str) -> str:
    return optimize_background_prompt(prompt)
