from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.filters.admin_protect import AdminProtect
from app.keyboards.s_admin import stats_kb
from app.database.database import async_session
from app.services.stats import get_all_usernames, calculate_conversion

admin_stats = Router()


@admin_stats.callback_query(AdminProtect(), F.data == "admin_stats")
async def show_stats_menu(callback: CallbackQuery):
    """Показывает меню статистики."""
    await callback.message.answer("Выберите действие", reply_markup=stats_kb)


@admin_stats.callback_query(AdminProtect(), F.data == "conversion")
async def show_conversion(callback: CallbackQuery):
    """Показывает конверсию."""
    async with async_session() as session:
        stats = await calculate_conversion(session)
    await callback.message.answer(stats)


@admin_stats.callback_query(AdminProtect(), F.data == "get_all_users")
async def show_all_users(callback: CallbackQuery):
    """Выводит список никнеймов пользователей (без админов), разбивая на части при необходимости."""
    async with async_session() as session:
        usernames = await get_all_usernames(session)

    if not usernames:
        await callback.message.answer("❌ В базе нет пользователей.")
        return

    # Telegram ограничение: 4096 символов в одном сообщении
    chunk_size = 4000  # С запасом
    user_text = " ".join(usernames)

    for i in range(0, len(user_text), chunk_size):
        await callback.message.answer(user_text[i:i+chunk_size])
