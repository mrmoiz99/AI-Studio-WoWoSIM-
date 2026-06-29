from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent / "prompt_templates"

DEFAULT_TEMPLATES = {
    "Destination Highlight": """
Create a realistic premium travel photography background.
The image should feel like a luxury destination campaign with clean negative space.
Use a simple composition, warm natural light, and a clear focal point.
""".strip(),
    "Travel Tip": """
Create a realistic travel lifestyle background for a useful travel tip.
Show a traveler, smartphone, airport, city, map, or destination detail without any readable screen text.
Keep the scene clean and practical.
""".strip(),
    "FIFA / Event Travel": """
Create a realistic event travel background with football energy and international travel atmosphere.
Show fans, stadium surroundings, travel city, or smartphone sharing moment.
Keep the composition clean and premium, not crowded.
""".strip(),
    "Discount Offer": """
Create a clean premium travel shopping/offer background.
Use simple destination or phone imagery with plenty of space for app-added promotion text.
Avoid crowded scenes.
""".strip(),
    "Breaking Trend": """
Create a realistic editorial travel background for a timely trend.
Make it clean, newsworthy, and brand-safe with enough space for headline overlay.
""".strip(),
}


def ensure_prompt_templates():
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in DEFAULT_TEMPLATES.items():
        path = PROMPT_DIR / f"{name.lower().replace(' / ', '_').replace(' ', '_')}.md"
        if not path.exists():
            path.write_text(content + "\n", encoding="utf-8")


def load_template(template_name: str) -> str:
    ensure_prompt_templates()
    filename = f"{(template_name or 'Destination Highlight').lower().replace(' / ', '_').replace(' ', '_')}.md"
    path = PROMPT_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return DEFAULT_TEMPLATES["Destination Highlight"]
