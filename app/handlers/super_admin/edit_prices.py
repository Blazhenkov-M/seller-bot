from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.filters.admin_protect import AdminProtect
from app.keyboards.s_admin import prices_kb

from app.database.database import async_session
from app.services.edit_prices import get_prices, update_price
from app.states import EditPriceState

s_admin_edit_prices = Router()


@s_admin_edit_prices.callback_query(AdminProtect(), F.data == "edit_prices")
async def edit_prices(callback: CallbackQuery):
    async with async_session() as session:
        prices = await get_prices(session)
        text = (
            f"💰 Текущие цены:\n"
            f"📅 Подписка (месяц): {prices.subscription} руб.\n"
            f"👨‍⚕️ Консультация: {prices.consultation} руб.\n"
            f"\nВыберите, какую цену изменить:"
        )

    await callback.message.answer(text, reply_markup=prices_kb)
    await callback.answer()


@s_admin_edit_prices.callback_query(AdminProtect(), F.data == "subscribe_month_price")
async def change_subscription_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите новую цену за подписку (месяц):")
    await state.set_state(EditPriceState.subscription)
    await callback.answer()


@s_admin_edit_prices.callback_query(AdminProtect(), F.data == "consultation_price")
async def change_consultation_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите новую цену за консультацию:")
    await state.set_state(EditPriceState.consultation)
    await callback.answer()


@s_admin_edit_prices.message(EditPriceState.subscription)
async def save_subscription_price(message: Message, state: FSMContext):
    try:
        new_price = int(message.text)
        async with async_session() as session:
            await update_price(session, "subscription", new_price)
        await message.answer(f"✅ Цена подписки обновлена: {new_price} руб.")
    except ValueError:
        await message.answer("❌ Ошибка: введите корректное число.")
    finally:
        await state.clear()


@s_admin_edit_prices.message(EditPriceState.consultation)
async def save_consultation_price(message: Message, state: FSMContext):
    try:
        new_price = int(message.text)
        async with async_session() as session:
            await update_price(session, "consultation", new_price)
        await message.answer(f"✅ Цена консультации обновлена: {new_price} руб.")
    except ValueError:
        await message.answer("❌ Ошибка: введите корректное число.")
    finally:
        await state.clear()
