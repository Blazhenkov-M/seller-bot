from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.filters.admin_protect import AdminProtect
from app.states import Newsletter
from app.services.newsletter import get_users
from app.keyboards.super_admin import cancel_send_all
from app.database.database import async_session
from app.core.bot_instance import bot

admin_newsletter = Router()


@admin_newsletter.callback_query(AdminProtect(), F.data == 'send_all')
async def newsletter_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.message)
    await callback.message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям',
                                  reply_markup=cancel_send_all)
    await callback.answer()


@admin_newsletter.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')

    async with async_session() as session:
        users = await get_users(session)

        for user in users:
            try:
                await bot.send_message(user.tg_id, message.text)
            except Exception as e:
                print(f"Ошибка при отправке пользователю {user.tg_id}: {e}")

    await message.answer('Рассылка успешно завершена.')
    await state.clear()


@admin_newsletter.callback_query(AdminProtect(), F.data == 'cancel_send_all')
async def cancel_newsletter(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Рассылка отменена.', reply_markup=None)
    await callback.answer()
