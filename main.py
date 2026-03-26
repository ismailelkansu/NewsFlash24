import asyncio
import logging
from telegram.ext import Application, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN, FETCH_INTERVAL
from database import (init_db, is_posted, mark_posted,
                      add_pending, get_pending, delete_pending,
                      update_pending_message_id)
from fetcher import fetch_articles
from filter import is_trusted_source
from formatter import format_article, build_message
from telegram_bot import post_to_channel, send_for_approval
from discord_bot import post_to_discord

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def process_articles():
    logger.info("Checking for new articles...")
    articles = fetch_articles()

    for article in articles:
        url = article["url"]
        title = article["title"]

        if is_posted(url):
            continue

        formatted = format_article(title, article.get("summary", ""), article["source"])
        message = build_message(
            title=title,
            summary=formatted["summary"],
            hashtags=formatted["hashtags"],
            url=url,
            source=article["source"]
        )

        if is_trusted_source(article["source_url"], article["source"]):
            tg_ok = await post_to_channel(message)
            dc_ok = await post_to_discord(message)
            if tg_ok or dc_ok:
                mark_posted(url, title)
                logger.info(f"Auto-posted: {title[:60]}")
        else:
            pending_id = add_pending(
                url=url,
                title=title,
                summary=formatted["summary"],
                hashtags=formatted["hashtags"],
                source=article["source"],
                original_link=url
            )
            if pending_id:
                msg_id = await send_for_approval(pending_id, message)
                if msg_id:
                    update_pending_message_id(pending_id, msg_id)
                logger.info(f"Sent for approval: {title[:60]}")

        await asyncio.sleep(1)


async def handle_approval(update, context):
    query = update.callback_query
    await query.answer()

    action, pending_id_str = query.data.split("_", 1)
    pending_id = int(pending_id_str)

    pending = get_pending(pending_id)
    if not pending:
        await query.edit_message_text("Already processed or not found.")
        return

    # columns: id, url, title, summary, hashtags, source, original_link, telegram_message_id, created_at
    url, title, summary, hashtags, source = pending[1], pending[2], pending[3], pending[4], pending[5]

    if action == "approve":
        message = build_message(title, summary, hashtags, url, source)
        tg_ok = await post_to_channel(message)
        dc_ok = await post_to_discord(message)
        if tg_ok or dc_ok:
            mark_posted(url, title)
            delete_pending(pending_id)
            await query.edit_message_text(f"✅ Posted:\n{title}")
        else:
            await query.edit_message_text(f"❌ Failed to post:\n{title}")
    else:
        mark_posted(url, title)
        delete_pending(pending_id)
        await query.edit_message_text(f"🗑 Rejected:\n{title}")


async def fetch_loop():
    while True:
        try:
            await process_articles()
        except Exception as e:
            logger.error(f"Fetch loop error: {e}")
        await asyncio.sleep(FETCH_INTERVAL)


async def main():
    init_db()
    logger.info("NewsFlash24 started.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_approval))

    async with app:
        await app.start()
        await app.updater.start_polling()
        await fetch_loop()
        await app.updater.stop()
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
