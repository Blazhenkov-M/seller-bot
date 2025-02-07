import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from database.init_data import initialize_data
from core.bot_instance import bot

from handlers.user import start, pay, load_report
from handlers.admin import admin
from handlers.super_admin import super_admin

from settings.logger_config import get_logger
logger = get_logger(__name__)

storage = RedisStorage.from_url("redis://localhost:6379")


async def main():
    logger.info("Starting bot. . .")

#    await initialize_data()
    dp = Dispatcher(storage=storage)
    dp.include_routers(start.start_router, pay.pay_router, load_report.load_router,
                       admin.admin, super_admin.super_admin)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error while starting bot: {e}")
