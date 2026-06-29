from ai.ollama import call_ollama
from ai.prompts import brand_context

def build_campaign(brief, model='llama3.1:latest'):
    prompt = f'''
You are building a complete WoWoSIM marketing campaign.
Brand memory:
{brand_context()}

Campaign brief:
{brief}

Generate:
1. Campaign idea
2. Instagram post
3. Facebook post
4. LinkedIn post
5. Reel script
6. Email concept
7. Hashtags
8. Image prompts
9. Posting calendar for 7 days
'''
    return call_ollama(prompt, model=model, timeout=360)
