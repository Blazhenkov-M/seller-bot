from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.database import async_session
from app.database.models import Subscription
from sqlalchemy.future import select

from app.services.add_user import add_user
from app.services.get_texts import get_text

from app.keyboards.user import start_kb, main_kb

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        # Добавляем пользователя, если его нет
        await add_user(tg_id=tg_id, username=username, session=session)

        # Запрашиваем подписку
        subscription = await session.execute(
            select(Subscription).where(Subscription.user_id == tg_id)
        )
        subscription = subscription.scalars().first()

        # Проверяем статус подписки
        if subscription and subscription.status:
            start_msg = "✅ У вас активна подписка!"
            reply_markup = main_kb
        else:
            start_msg = await get_text(session, "start")  # Загружаем текст из БД
            reply_markup = start_kb

    await message.answer(start_msg, reply_markup=reply_markup)
    await state.clear()
