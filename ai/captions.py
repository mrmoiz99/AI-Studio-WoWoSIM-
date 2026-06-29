from ai.ollama import call_ollama
from ai.prompts import brand_context

def generate_social_post(trend, platform='Instagram', model='llama3.1:latest'):
    prompt = f'''
You are the social media strategist for WoWoSIM.

Brand memory:
{brand_context()}

Trend: {trend}
Platform: {platform}

Create a complete social post.
Return exactly:
TITLE:
CAPTION:
HASHTAGS:
IMAGE PROMPT:

Rules:
- Caption must be 40 to 90 words.
- Naturally connect the trend to travel, eSIM data, airport connectivity, maps, events, or staying online abroad.
- Hashtags: 8 to 12.
- Image prompt must describe only the background visual. Do not ask for text, logo, readable words, or final ad layout. Mention clean travel/eSIM scene, smartphone/connectivity if useful, empty space for overlay, orange #FF5F00 and white as subtle accents.
'''
    return call_ollama(prompt, model=model, timeout=240)
