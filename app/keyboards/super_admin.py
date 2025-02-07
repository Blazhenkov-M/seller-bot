from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


super_admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💰 Цены", callback_data="admin_prices")],
    [InlineKeyboardButton(text="👔 Сотрудники", callback_data="admin_prices")],
    [InlineKeyboardButton(text="📋 Тексты", callback_data="texts")],
    [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
    [InlineKeyboardButton(text="📩 Рассылка всем", callback_data="send_all")],
    [InlineKeyboardButton(text="💬 Ответ пользователю", callback_data="response_user")]])

admins_edit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📜 Список", callback_data="worker_list")],
    [InlineKeyboardButton(text="✅ Добавить", callback_data="add_worker")],
    [InlineKeyboardButton(text="❌ Удалить", callback_data="del_worker")]])

prices_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подписка месяц", callback_data="subscribe_month_price")],
    [InlineKeyboardButton(text="Консультация", callback_data="consultation_price")]])

