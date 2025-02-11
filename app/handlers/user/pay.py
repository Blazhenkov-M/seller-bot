from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import LabeledPrice, PreCheckoutQuery, SuccessfulPayment

from app.core.bot_instance import bot
from app.keyboards.user import pay_kb, load_xl_kb
from app.texts import START_PAY_MSG
from app.services.subscription_update import update_subscription_status
from app.services.get_prices_for_pay import get_prices_for_pay
from app.database.database import async_session
pay_router = Router()

#  live_ORehkMOxK1kZmrW9ZzIlugIzIrT6devepT0bThyEz_k
PROVIDER_TOKEN = "381764678:TEST:110835"


@pay_router.callback_query(F.data == "payment")
async def start_pay(callback: CallbackQuery):
    await callback.message.answer(START_PAY_MSG, reply_markup=pay_kb)


@pay_router.callback_query(F.data == "payment_start")
async def send_invoice(callback: CallbackQuery):
    async with async_session() as session:
        subscription_price, _ = await get_prices_for_pay(session)  # Берем только цену подписки

    if subscription_price is None:
        await callback.message.answer("Ошибка: цена подписки не найдена.")
        return

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Оплата подписки",
        description="Тестовый платеж",
        payload="subscription_payment",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=subscription_price * 100)],
    )


@pay_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@pay_router.message(F.successful_payment)
async def successful_payment_handler(msg: Message):
    payment_info = msg.successful_payment
    transaction_id = payment_info.provider_payment_charge_id  # ID транзакции в ЮKassa
    user_id = msg.from_user.id  # Telegram ID пользователя

    async with async_session() as session:  # Используем async_session из твоего кода
        await update_subscription_status(user_id, session)

    await msg.answer(f"✅ Оплата прошла успешно!\nID транзакции: {transaction_id}")
    await msg.answer("Загрузите отчет с маркетплейса", reply_markup=load_xl_kb)
