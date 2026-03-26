import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, TELEGRAM_ADMIN_ID

logger = logging.getLogger(__name__)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def post_to_channel(message: str) -> bool:
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
        return True
    except Exception as e:
        logger.error(f"Telegram post error: {e}")
        return False

async def send_for_approval(pending_id: int, message: str):
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pending_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pending_id}"),
    ]]
    try:
        msg = await bot.send_message(
            chat_id=TELEGRAM_ADMIN_ID,
            text=f"⚠️ *Approval needed:*\n\n{message}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return msg.message_id
    except Exception as e:
        logger.error(f"Telegram approval send error: {e}")
        return None
