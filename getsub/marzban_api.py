import logging
import datetime as dt

from marzban import MarzbanAPI, MarzbanTokenCache, ProxySettings, UserCreate, UserModify
from getsub.config import settings

logger = logging.getLogger(__name__)

api = MarzbanAPI(base_url=settings.PANEL_URL)

token = MarzbanTokenCache(
    client=api,
    username=settings.PANEL_USER, password=settings.PANEL_PASSWORD,
    token_expire_minutes=1440  # DEFAULT VALUE (Optional argument)
)

def check_login():
    token = api.get_token(username=settings.PANEL_USER, password=settings.PANEL_PASSWORD)
    return token

async def check_templates(templates: list):
    print("hehe")

async def get_subscription(username: str, tg_uid: int = 0):
    users = await api.get_users(token=await token.get_token(), username=username)

    if users.total == 0:
        logger.info("Searching in notes")
        users = await api.get_users(token=await token.get_token(), search=f"tg_uid: {tg_uid}")

    match users.total:
        case 1:
            logger.info(f"User found '{users.users[0].username}' (TG UID: {tg_uid})")
            return users.users[0]
        case 0:
            logger.info(f"User NOT found for TG UID: {tg_uid}")
            return None
        case _:
            logger.error(f"Multiple users found for TG UID: {tg_uid}")
            raise

async def get_template(template_name: str):
    templates = await api.get_user_templates(token=await token.get_token())
    return next((x for x in templates if x.name == template_name), None)

async def create_user_by_template(username: str, tg_uid: int, template_name: str, reset_strategy: str):
    template = await get_template(template_name)
    logger.debug("Effective template {template}")
    new_user = UserCreate(
        username=username,
        data_limit=template.data_limit,
        data_limit_reset_strategy=reset_strategy,
        expire=0 if template.expire_duration == 0 else int(dt.datetime.now().timestamp()) + template.expire_duration,
        inbounds=template.inbounds,
        note=f"tg_uid: {tg_uid}",
        proxies={"vless": ProxySettings(flow="xtls-rprx-vision")}
    )
    logger.debug(f"Creating user {new_user}")
    created_user = await api.add_user(user=new_user, token=await token.get_token())
    logger.info(f"User {created_user.username} created for TG UID: {tg_uid}")
    logger.debug(f"Created user {created_user}")

async def prolong_user(username, template_name):
    user = await get_subscription(username)
    template = await get_template(template_name)
    logger.debug(f"Effective template {template}")

    if user.status == "expired":
        logger.debug("Expited user. Addding to now")
        new_expire = int(dt.datetime.now().timestamp()) + template.expire_duration
    else:
        logger.debug("Active user. Addding to current expire")
        new_expire = user.expire + template.expire_duration

    modified_user = await api.modify_user(
        username=username, 
        user=UserModify(expire=new_expire),
        token=await token.get_token()
        )
    logger.debug(f"Modified user {modified_user}")
    pass
