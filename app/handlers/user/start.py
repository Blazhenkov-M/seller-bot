from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.database import async_session
from app.services.user import add_user

from app.keyboards.start import start_kb
from app.services.get_texts import get_text
start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        await add_user(tg_id=tg_id, username=username, session=session)
        start_msg = await get_text(session, "start")  # Загружаем текст из БД

    await message.answer(start_msg, reply_markup=start_kb)
    await state.clear()
