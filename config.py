import os

# Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-8b-8192"

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")  # e.g. @NewsFlash24
TELEGRAM_ADMIN_ID = os.environ.get("TELEGRAM_ADMIN_ID", "")      # Your personal Telegram user ID

# Discord
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

# RSS Feeds
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://rss.cnn.com/rss/edition_world.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.theguardian.com/theguardian/world/rss",
    "https://apnews.com/rss/apf-topnews",
]

# Trusted sources — auto post without approval
TRUSTED_SOURCES = [
    "bbc", "reuters", "cnn", "aljazeera", "guardian",
    "bloomberg", "apnews", "ap.org", "nytimes", "washingtonpost"
]

# How often to check for new articles (seconds)
FETCH_INTERVAL = 300  # 5 minutes
