import json
from config import BRAND_MEMORY_PATH

def load_brand_memory():
    try:
        return json.loads(BRAND_MEMORY_PATH.read_text(encoding='utf-8'))
    except Exception:
        return {}

def brand_context():
    b = load_brand_memory()
    return json.dumps(b, indent=2, ensure_ascii=False)
