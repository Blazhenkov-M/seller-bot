import logging

import keyboards.admin_kb
from services.user import get_users

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import user_kb as kb
from handlers.admin.admin import AdminProtect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

admin_newsletter = Router()


class Newsletter(StatesGroup):
    message = State()


@admin_newsletter.callback_query(AdminProtect(), F.data == 'send_all')
async def newsletter_start(callback: CallbackQuery, state: FSMContext):
    logger.info("Newsletter process started by user: %s", callback.from_user.id)
    await state.set_state(Newsletter.message)
    await callback.message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям',
                                  reply_markup=keyboards.admin_kb.cancel_admin_keyboard)
    await callback.answer()


@admin_newsletter.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    logger.info("Newsletter message received: %s by user: %s", message.text, message.from_user.id)
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except Exception as e:
            logger.error("Error sending newsletter to user: %s, error: %s", user.tg_id, e)
    await message.answer('Рассылка успешно завершена.')
    await state.clear()


@admin_newsletter.callback_query(AdminProtect(), F.data == 'cancel_send_all')
async def cancel_newsletter(callback: CallbackQuery, state: FSMContext):
    logger.info("Newsletter process canceled by user: %s", callback.from_user.id)
    await state.clear()
    await callback.message.edit_text('Рассылка отменена.', reply_markup=None)
    await callback.answer()
