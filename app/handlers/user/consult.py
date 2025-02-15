from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.database import async_session
from app.services.get_consult_price import get_consult_price


consult_router = Router()


@consult_router.callback_query(F.data == "get_cosult")
async def request_consult(callback: CallbackQuery):
    """Обрабатывает запрос на консультацию."""
    async with async_session() as session:
        price = await get_consult_price(session)

    if price is None:
        await callback.message.answer("❌ Ошибка: цена консультации не найдена.")
        return

    text = f"💡 Консультация стоит {price} ₽. Напишите @super_kamila"

    await callback.message.answer(text)
