from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.admin_protect import AdminProtect
from keyboards.admin import admin_kb

admin = Router()


@admin.message(AdminProtect("admin"), Command('admin'))
async def admin_menu(message: Message):
    await message.answer('Привет, админ!', reply_markup=admin_kb)
