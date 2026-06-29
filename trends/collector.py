import feedparser
from config import TREND_SOURCES
from trends.trend_score import simple_score
from database.database import insert_trend

def collect_trends(max_per_source=10):
    collected = []
    seen = set()
    for source, url in TREND_SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_per_source]:
            title = (entry.get('title') or '').strip()
            if not title or title.lower() in seen or title.lower() == 'daily search trends':
                continue
            seen.add(title.lower())
            link = entry.get('link') or ''
            score = simple_score(title)
            insert_trend(title, source, link, score)
            collected.append({'title': title, 'source': source, 'url': link, 'score': score})
    return collected
