from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="payment")],
    [InlineKeyboardButton(text="💬 Задать вопрос", url="https://t.me/super_kamila/")]])

pay_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Далее", callback_data="payment_start")]
])

get_pay_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оплатить", callback_data="payment_start")]
])

load_xl_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📎 Загрузить", callback_data="load_report")]
])

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📎 Загрузить отчет", callback_data="load_report")],
    [InlineKeyboardButton(text="🚀 Запрос на консультацию", callback_data="get_cosult")],
    [InlineKeyboardButton(text="💬 Задать вопрос", url="https://t.me/super_kamila/")]])

