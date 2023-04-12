import asyncio
import logging

from tgbot.filters.admin import AdminFilter
from tgbot.filters.subscriber_check import IsSubscriber
from tgbot.handlers.echo import register_echo

# from tgbot.handlers.faq import register_faq
from tgbot.handlers.user import register_user
from tgbot.handlers.catalog import register_catalog
from tgbot.handlers.shopping_cart import register_shopping_cart
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.models import db_funcs_sql

from loader import bot, dp, config, db, wb

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsSubscriber)


def register_all_handlers(dp):
    # register_admin(dp)
    register_user(dp)
    register_catalog(dp)
    register_shopping_cart(dp)
    # register_faq(dp)
    from tgbot.handlers import faq

    # register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    bot["config"] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        # await db_gino.on_startup(dp)
        await db_funcs_sql.on_startup(db)
        await dp.start_polling()
    finally:
        await wb.close()
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
