import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    InvalidCallbackData,
)
import logging

from getsub.config import settings
from getsub.marzban_api import check_login
from getsub.router import router
from getsub.menu import start
from getsub.utils import handle_invalid_button

logger = logging.getLogger(__name__)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # run the login coroutine on that loop (do NOT use asyncio.run here)
    loop.run_until_complete(check_login())

    application = (
        ApplicationBuilder()
        .token(settings.BOT_TOKEN)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData))
    application.add_handler(CallbackQueryHandler(router))
    
    logger.info("Starting the bot...")

    if settings.get('WEBHOOK_URL'):
        logger.warning(f"Running in webhook mode on {settings.WEBHOOK_URL}{settings.WEBHOOK_URL_PATH}")
        application.run_webhook(
            listen=settings.WEBHOOK_LISTEN,
            port=settings.WEBHOOK_PORT,
            webhook_url=settings.WEBHOOK_URL,
            url_path=settings.WEBHOOK_URL_PATH,
        )
    else:
        logger.warning("No WEBHOOK_URL specified, running in non-webhook mode")
        application.run_polling()


if __name__ == '__main__':
    main()
