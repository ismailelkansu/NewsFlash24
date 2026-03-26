import logging
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)
client = Groq(api_key=GROQ_API_KEY)

def format_article(title: str, raw_summary: str, source: str) -> dict:
    prompt = f"""You are a news editor. Given this news article, create:
1. A 2-3 sentence English summary (clear, concise, no fluff)
2. 3-5 relevant hashtags

Article Title: {title}
Raw Content: {raw_summary[:500]}
Source: {source}

Respond in this exact format (nothing else):
SUMMARY: [your 2-3 sentence summary]
HASHTAGS: #tag1 #tag2 #tag3"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3,
        )
        text = response.choices[0].message.content.strip()

        summary = ""
        hashtags = ""
        for line in text.split("\n"):
            if line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
            elif line.startswith("HASHTAGS:"):
                hashtags = line.replace("HASHTAGS:", "").strip()

        return {
            "summary": summary or title,
            "hashtags": hashtags or "#BreakingNews #WorldNews"
        }
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return {
            "summary": title,
            "hashtags": "#BreakingNews #WorldNews"
        }

def build_message(title: str, summary: str, hashtags: str, url: str, source: str) -> str:
    return (
        f"🔴 *{title}*\n\n"
        f"{summary}\n\n"
        f"{hashtags}\n\n"
        f"🔗 [Read more]({url})\n"
        f"📰 Source: {source}"
    )
