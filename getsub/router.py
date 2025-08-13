from telegram import InputMediaPhoto, Update
from telegram.ext import CallbackContext

from getsub.billing import billing
from getsub.menu import restart
from getsub.subscription import subscription, sub_option, sub_prolong

import logging

from getsub.utils import under_construction

logger = logging.getLogger(__name__)

async def router(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Always answer the callback query to stop the loading indicator

    logger.info(f"User {query.from_user.id} going to -- {query.data}")
    match query.data[-1].split(':')[0]:
        # menu
        case "restart":
            await restart(query)
        case "subscription":
            await subscription(query)

        # subscription level
        case "sub_prolong":
            await sub_prolong(query)
        case "sub_option":
            await sub_option(query)
        case "billing":
            await billing(query)
        case _:
            logger.warning(f"Routed to the wrong place\n{query}")
