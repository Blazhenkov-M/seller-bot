from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.filters.admin_protect import AdminProtect
from app.keyboards.admin import admin_kb

admin = Router()


@admin.message(AdminProtect("admin"), Command('admin'))
async def admin_menu(message: Message):
    await message.answer('Привет, админ!', reply_markup=admin_kb)
