from getsub.marzban_api import create_user_by_template, get_subscription, prolong_user
from getsub.subscription import sub_thanks
from getsub.utils import generate_name
from getsub.config import settings

import logging

logger = logging.getLogger(__name__)

async def billing(query) -> None:
    history = query.data
    tg_uid = query.from_user.id
    sub_option = [item for item in settings.SUBSCRIPTION_OPTIONS if item["name"] == history[-1].split(':')[1]][0]

    sub_option_billing_type = history[-1].split(':')[2]
    match sub_option_billing_type:
        case 'free':
            # Some real payment logic
            logger.info(f"Free purchase of {sub_option['name']} by TG UID: {tg_uid}")
            await billing_finalize(query, tg_uid, sub_option['template_name'], sub_option['reset_strategy'])
        case _:
            logger.error("Not implemented")

async def billing_finalize(query, tg_uid, template_name, reset_strategy):
    user = await get_subscription(generate_name(tg_uid))
    if user:
        await prolong_user(user.username, template_name, reset_strategy)
    else:
        await create_user_by_template(generate_name(tg_uid), template_name, reset_strategy)

    await sub_thanks(query)
