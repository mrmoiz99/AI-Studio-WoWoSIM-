from ai.ollama import call_ollama
from ai.prompts import brand_context

def generate_seo_blog(keyword, destination='', model='llama3.1:latest'):
    prompt = f'''
Write an SEO-ready WoWoSIM blog draft.
Brand memory:
{brand_context()}

Main keyword: {keyword}
Destination/region: {destination}

Return:
SEO TITLE
META DESCRIPTION
URL SLUG
OUTLINE
BLOG DRAFT
FAQS
IMAGE ALT TEXT
IMAGE PROMPTS

Keep it useful and human. Avoid unsupported pricing claims.
'''
    return call_ollama(prompt, model=model, timeout=600)
