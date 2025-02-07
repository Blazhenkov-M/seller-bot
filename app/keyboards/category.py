from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_category_keyboard(selected_categories: dict) -> InlineKeyboardMarkup:
    buttons = []

    for category, is_selected in selected_categories.items():
        emoji = "✅" if is_selected else "⬜"
        buttons.append([InlineKeyboardButton(text=f"{emoji} {category}", callback_data=f"category_{category}")])

    buttons.append([InlineKeyboardButton(text="✏️ Добавить категорию", callback_data="add_category")])
    buttons.append([InlineKeyboardButton(text="✅ Подтвердить выбор", callback_data="confirm_categories")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
