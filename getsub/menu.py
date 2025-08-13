from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
)
from getsub.config import settings
import logging

logger = logging.getLogger(__name__)

start_text="Выберите пункт меню:"
start_keyboard_buttons = [
        [InlineKeyboardButton("Моя подписка", callback_data=["subscription"])],
    ]
if settings.get('SUPPORT_LINK'):
    start_keyboard_buttons += [[InlineKeyboardButton("Поддержка", url=settings.SUPPORT_LINK)]]

async def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(start_keyboard_buttons)
    await update.message.reply_text(
        f"Приветствую! {start_text}", reply_markup=reply_markup
    )

async def restart(query) -> None:
    reply_markup = InlineKeyboardMarkup(start_keyboard_buttons)
    await query.edit_message_text(text=f"{start_text}", reply_markup=reply_markup)
