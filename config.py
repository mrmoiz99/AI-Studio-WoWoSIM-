from pathlib import Path
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "wowosim.db"
BRAND_MEMORY_PATH = BASE_DIR / "brand" / "brand_memory.json"
IMAGE_DIR = BASE_DIR / "storage" / "generated_images"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
LOG_DIR = BASE_DIR / "storage" / "logs"

# Environment fallback only. The Settings page can store API keys locally in SQLite.
ENV_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""

DEFAULT_MODELS = {
    "trend_research": "qwen3:8b",
    "research": "qwen3:8b",
    "campaign_planner": "llama3.1:latest",
    "scene_planner": "llama3.1:latest",
    "social_posts": "llama3.1:latest",
    "seo_blog": "llama3.1:latest",
    "campaign_builder": "llama3.1:latest",
    "image_prompt": "llama3.1:latest",
}

TREND_SOURCES = {
    "Google Trends Worldwide": "https://trends.google.com/trending/rss",
    "Google Trends USA": "https://trends.google.com/trending/rss?geo=US",
    "Google News Travel": "https://news.google.com/rss/search?q=travel%20OR%20tourism%20OR%20airport%20OR%20visa&hl=en-US&gl=US&ceid=US:en",
    "Reddit Travel": "https://www.reddit.com/r/travel/.rss",
}
