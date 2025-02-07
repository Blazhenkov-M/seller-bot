from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.database import async_session
from services.user import add_user

from keyboards.start import start_kb
from texts import START_MSG
start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with async_session() as session:
        await add_user(tg_id=tg_id, username=username, session=session)

    await message.answer(START_MSG, reply_markup=start_kb)
    await state.clear()
