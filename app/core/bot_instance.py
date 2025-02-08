from aiogram import Bot
from app.settings.config import settings


bot = Bot(token=settings.bot_token.get_secret_value())
