from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💬 Ответ пользователю", callback_data="response_user")]])
