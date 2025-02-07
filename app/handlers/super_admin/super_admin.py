from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.admin_protect import AdminProtect
from keyboards.super_admin import super_admin_kb

super_admin = Router()


@super_admin.message(AdminProtect("superadmin"), Command('apanel'))
async def admin_menu(message: Message):
    await message.answer('Привет, супер-админ!', reply_markup=super_admin_kb)
