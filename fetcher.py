import feedparser
import logging
from config import RSS_FEEDS

logger = logging.getLogger(__name__)

def fetch_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                article = {
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", "").strip(),
                    "summary": entry.get("summary", "").strip(),
                    "source": feed.feed.get("title", feed_url),
                    "source_url": feed_url,
                }
                if article["title"] and article["url"]:
                    articles.append(article)
        except Exception as e:
            logger.error(f"Error fetching {feed_url}: {e}")
    return articles
