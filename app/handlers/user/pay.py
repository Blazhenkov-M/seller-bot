from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import LabeledPrice, PreCheckoutQuery, SuccessfulPayment

from core.bot_instance import bot
from keyboards.start import pay_kb, load_xl_kb
from texts import START_PAY_MSG
pay_router = Router()

#  live_ORehkMOxK1kZmrW9ZzIlugIzIrT6devepT0bThyEz_k
PROVIDER_TOKEN = "381764678:TEST:110835"


@pay_router.callback_query(F.data == "payment")
async def start_pay(callback: CallbackQuery):
    await callback.message.answer(START_PAY_MSG, reply_markup=pay_kb)


@pay_router.callback_query(F.data == "payment_start")
async def send_invoice(callback: CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Оплата подписки",
        description="Тестовый платеж",
        payload="ыыы",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Подписка", amount=500000)],
    )


@pay_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@pay_router.message(F.successful_payment)
async def successful_payment_handler(msg: Message):
    payment_info = msg.successful_payment
    transaction_id = payment_info.provider_payment_charge_id  # ID транзакции в ЮKassa

    await msg.answer(f"✅ Оплата прошла успешно!\nID транзакции: {transaction_id}")
    await msg.answer("Загрузите отчет с маркетплейса", reply_markup=load_xl_kb)
