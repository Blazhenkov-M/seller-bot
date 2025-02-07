from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="payment")],
    [InlineKeyboardButton(text="💬 Задать вопрос", url="https://t.me/super_kamila/")]])

pay_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Далее", callback_data="payment_start")]
])

load_xl_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📎 Загрузить", callback_data="load_report")]
])
