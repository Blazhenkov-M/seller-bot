from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.filters.admin_protect import AdminProtect
from app.keyboards.super_admin import edit_texts_kb

from app.database.database import async_session
from app.services.edit_texts import update_message_content
from app.states import EditMessageState

s_admin_edit_texts = Router()


@s_admin_edit_texts.callback_query(AdminProtect(), F.data == "edit_texts")
async def edit_texts(callback: CallbackQuery):
    """Выбор сообщения для редактирования."""
    await callback.message.answer("Выберите сообщение для редактирования:", reply_markup=edit_texts_kb)
    await callback.answer()


@s_admin_edit_texts.callback_query(AdminProtect(), F.data == "edit_text_start")
async def edit_start_message(callback: CallbackQuery, state: FSMContext):
    """Запрашивает новый текст для 'start'."""
    await callback.message.answer("Введите новый текст для 'start':")
    await state.set_state(EditMessageState.start)
    await callback.answer()


@s_admin_edit_texts.callback_query(AdminProtect(), F.data == "edit_text_load_report")
async def edit_load_report_message(callback: CallbackQuery, state: FSMContext):
    """Запрашивает новый текст для 'load_report'."""
    await callback.message.answer("Введите новый текст для 'load_report':")
    await state.set_state(EditMessageState.load_report)
    await callback.answer()


@s_admin_edit_texts.message(EditMessageState.start)
async def save_start_message(message: Message, state: FSMContext):
    """Сохраняет новый текст для 'start'."""
    async with async_session() as session:
        updated_message = await update_message_content(session, "start", message.text)

    if updated_message:
        await message.answer(f"✅ Текст 'start' успешно обновлён.")
    else:
        await message.answer("❌ Ошибка: сообщение 'start' не найдено.")

    await state.clear()


@s_admin_edit_texts.message(EditMessageState.load_report)
async def save_load_report_message(message: Message, state: FSMContext):
    """Сохраняет новый текст для 'load_report'."""
    async with async_session() as session:
        updated_message = await update_message_content(session, "load_report", message.text)

    if updated_message:
        await message.answer(f"✅ Текст 'load_report' успешно обновлён.")
    else:
        await message.answer("❌ Ошибка: сообщение 'load_report' не найдено.")

    await state.clear()
