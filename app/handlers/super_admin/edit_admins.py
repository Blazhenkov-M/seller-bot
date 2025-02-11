from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.states import AddAdminState, RemoveAdminState
from app.filters.admin_protect import AdminProtect
from app.keyboards.s_admin import admins_edit_kb

from app.database.database import async_session
from app.services.edit_admins import get_admins_list, add_admin, remove_admin

s_admin_edit_admins = Router()


@s_admin_edit_admins.callback_query(AdminProtect(), F.data == "edit_workers")
async def edit_workers(callback: CallbackQuery):
    await callback.message.answer("Выберите действие", reply_markup=admins_edit_kb)


@s_admin_edit_admins.callback_query(AdminProtect(), F.data == "worker_list")
async def workers_list(callback: CallbackQuery):
    """Выводит список никнеймов админов"""
    async with async_session() as session:
        admins = await get_admins_list(session)

    if admins:
        admins_list = "\n".join(admins)
        await callback.message.answer(f"Список админов:\n{admins_list}")
    else:
        await callback.message.answer("Вы пока не назначили ни одного администратора.")


@s_admin_edit_admins.callback_query(AdminProtect(), F.data == "add_admin")
async def ask_admin_username(callback: CallbackQuery, state: FSMContext):
    """Запрашивает никнейм нового админа у супер-админа"""
    await callback.message.answer("Введите никнейм пользователя, которого хотите сделать администратором:")
    await state.set_state(AddAdminState.waiting_for_username)


@s_admin_edit_admins.message(StateFilter(AddAdminState.waiting_for_username))
async def process_admin_username(message: Message, state: FSMContext):
    """Обрабатывает ввод никнейма и добавляет пользователя в админы"""
    username = message.text.strip()

    async with async_session() as session:
        result = await add_admin(username, session)

    if result is True:
        await message.answer(f"Пользователь @{username} теперь администратор!")
    elif result is None:
        await message.answer(f"Пользователь @{username} уже является администратором.")
    else:
        await message.answer(f"Пользователь @{username} не найден в базе.")

    await state.clear()  # Сбрасываем состояние


"""Удаление админа"""
@s_admin_edit_admins.callback_query(AdminProtect(), F.data == "del_admin")
async def ask_admin_to_remove(callback: CallbackQuery, state: FSMContext):
    """Запрашивает никнейм админа для удаления"""
    await callback.message.answer("Введите никнейм администратора, которого хотите удалить:")
    await state.set_state(RemoveAdminState.waiting_for_username)


@s_admin_edit_admins.message(StateFilter(RemoveAdminState.waiting_for_username))
async def process_admin_removal(message: Message, state: FSMContext):
    """Обрабатывает удаление администратора"""
    username = message.text.strip()

    async with async_session() as session:
        result = await remove_admin(username, session)

    if result is True:
        await message.answer(f"Пользователь @{username} удален из администраторов.")
    elif result is None:
        await message.answer(f"Пользователь @{username} не является администратором.")
    else:
        await message.answer(f"Пользователь @{username} не найден в базе.")

    await state.clear()  # Сбрасываем состояние
