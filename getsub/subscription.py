from telegram import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from getsub.config import settings
from getsub.marzban_api import get_subscription, get_template
from getsub.utils import append_back
from getsub.utils import generate_name, humanize_duration, humanize_usage, humanize_timedelta

sub_info_text = """\
*Имя:* `{username}`
*Статус:* {status_text}

*Трафика за период:* {used_traffic} из {data_limit}
*Трафика всего:* {lifetime_used_traffic}
"""

async def sub_get_info(tg_uid: int, history: list):
    user_sub = await get_subscription(generate_name(tg_uid), tg_uid)
    if user_sub:

        if user_sub.status == "active":
            status_text = "активна"
            if user_sub.expire is not None:
                status_text += f" (еще {humanize_timedelta(user_sub.expire)})"

        elif user_sub.status == "expired":
            status_text = "истекла"
            if user_sub.expire is not None:
                status_text += f" ({humanize_timedelta(user_sub.expire)} назад)"
        else:
            status_text = user_sub.status

        text = sub_info_text.format(
            username=user_sub.username,
            status_text=status_text,
            used_traffic=humanize_usage(user_sub.used_traffic),
            data_limit="♾️" if user_sub.data_limit is None else humanize_usage(user_sub.data_limit),
            lifetime_used_traffic=humanize_usage(user_sub.lifetime_used_traffic),
        )
        keyboard = [[InlineKeyboardButton("Подписка (и инструкции)", url=user_sub.subscription_url)]]

        if user_sub.expire != None:
            keyboard += [[InlineKeyboardButton("Продлить", callback_data=(history + ["sub_prolong"]))]]
    else:
        keyboard = [[InlineKeyboardButton(f"{i+1}. {x['displayname']}", callback_data=(history + [f"sub_option:{x['name']}"]))] for i, x in enumerate(settings.SUBSCRIPTION_OPTIONS)]
        text="У вас нет подписки, выберите один из вариантов:"
    return (text, keyboard)

async def subscription(query) -> None:
    text, keyboard = await sub_get_info(query.from_user.id, query.data)
    keyboard=append_back(keyboard, query.data)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def sub_option(query) -> None:
    sub_option_text = """
Вариант *"{displayname}"*
*Пакет трафика:* {data_limit}
*Длительность:* {expire_duration}
"""
    history = query.data
    sub_option = [item for item in settings.SUBSCRIPTION_OPTIONS if item["name"] == history[-1].split(':')[1]][0]
    sub_option_template = await get_template(sub_option['template_name'])
    text = sub_option_text.format(
        displayname=sub_option['displayname'],
        data_limit="безлимит" if sub_option_template.data_limit == 0 else f"{sub_option_template.data_limit } в месяц",
        expire_duration="не ограничена" if sub_option_template.expire_duration == 0 else f"{humanize_duration(sub_option_template.expire_duration)}",
    )

    keyboard = [[
        InlineKeyboardButton(
            "Бесплатно"
            if x['billing_type'] == 'free'
            else f"{x['price']} {x['currency']} ({x['billing_type']})",
            callback_data=(history + [f"billing:{sub_option['name']}:{x['billing_type']}"])
        )
    ] for x in sub_option['billing']]

    keyboard=append_back(keyboard, history)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def sub_prolong(query):
    history = query.data

    text = "Выберите вариант продления:"
    keyboard = [[InlineKeyboardButton(f"{i+1}. {x['displayname']}", callback_data=(history + [f"sub_option:{x['name']}"]))] for i, x in enumerate(settings.SUBSCRIPTION_OPTIONS)]
    keyboard=append_back(keyboard, history)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)


async def sub_thanks(query):
    text="""
Спасибо!
Приятного использования!
"""
    keyboard = [[InlineKeyboardButton("Моя подписка", callback_data=(["subscription"]))]]
    keyboard += [[InlineKeyboardButton("Меню", callback_data=(["restart"]))]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)
