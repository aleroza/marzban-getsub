from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import ContextTypes
from codenamize import codenamize
import humanize
import datetime as dt

from getsub.config import settings
humanize.i18n.activate("ru_RU")

async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text("Простите, кнопка устарела 😕\nОтправьте /start и начнем с начала.")

async def handle_errors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the shit happened."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(f"Простите, произошла ошибка 😕\nМы постараемся сами её решить, но вы можете написать нам в поддержку {settings.SUPPORT_LINK}")

def generate_name(tg_uid: int) -> str:
    return codenamize(str(tg_uid)+settings.TG_UID_SALT)

def humanize_usage(bytes_num) -> str:
    return humanize.naturalsize(bytes_num, binary=True, format="%.2f")

def humanize_duration(seconds: int) -> str:
    return humanize.precisedelta(dt.timedelta(seconds=seconds))

def humanize_timedelta(unixtime: int) -> str:
    return humanize.precisedelta(dt.datetime.now() - dt.datetime.fromtimestamp(unixtime), minimum_unit='minutes', format="%0.0f")


def append_back(keyboard: list, history: list):
    history_temp = history.copy()
    history_temp.pop()
    if len(history_temp) == 0:
        history_temp.append('restart')
    keyboard.append([InlineKeyboardButton("Назад", callback_data=history_temp)])

    return keyboard

async def under_construction(query):
    photo_url = "https://st3.depositphotos.com/7863750/16166/i/1600/depositphotos_161665700-stock-photo-cat-builder-4.jpg"
    text = "Андер канстракшон\nВернись в меню /start"
    await query.edit_message_media(
        media=InputMediaPhoto(media=photo_url, caption=text),
    )
