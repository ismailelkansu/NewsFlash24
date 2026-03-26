import logging
import aiohttp
from config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)

async def post_to_discord(message: str) -> bool:
    if not DISCORD_WEBHOOK_URL:
        return False

    # Telegram Markdown → Discord format
    discord_message = message.replace("*", "**")

    payload = {
        "content": discord_message,
        "username": "NewsFlash24",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                return resp.status in (200, 204)
    except Exception as e:
        logger.error(f"Discord post error: {e}")
        return False
