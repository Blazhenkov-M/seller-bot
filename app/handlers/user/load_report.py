import os
import re
import pandas as pd
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import ReportStates
from app.database.database import async_session
from app.database.models import Expense, Order
from app.core.bot_instance import bot
from app.core.expense_categories import EXPENSE_CATEGORIES
from app.services.notify_admins import notify_admins
from app.keyboards.user import main_kb

load_router = Router()

VALID_KEYWORDS_1 = {"Номер поставки", "Предмет", "Код номенклатуры", "дата продажи"}
VALID_KEYWORDS_2 = {"товар", "штрих-код товара"}


def clean_text(text):
    """Очищает текст от пробелов, невидимых символов и приводит к нижнему регистру."""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)  # Убираем двойные пробелы
    text = text.replace("\xa0", " ")  # Убираем неразрывные пробелы
    return text


def find_header_row(df):
    """Ищет строку, где находятся заголовки."""
    valid_keywords_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_1 | VALID_KEYWORDS_2}

    best_row = -1
    max_hits = 0

    for i in range(min(20, len(df))):  # Проверяем первые 20 строк (на всякий случай)
        row_values = {clean_text(str(val)) for val in df.iloc[i].dropna().values}
        matches = len(valid_keywords_lower & row_values)  # Сколько совпадений

        if matches > max_hits:
            max_hits = matches
            best_row = i

    return best_row if max_hits > 0 else None  # Если вообще ничего не нашли, вернем None


def contains_valid_keywords(df):
    """Проверяет, содержатся ли ключевые слова в заголовках таблицы."""
    headers = {clean_text(col) for col in df.columns}

    valid_keywords_1_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_1}
    valid_keywords_2_lower = {kw.lower().strip() for kw in VALID_KEYWORDS_2}

    found_1 = [kw for kw in valid_keywords_1_lower if kw in headers]
    found_2 = [kw for kw in valid_keywords_2_lower if kw in headers]

    print("Найденные ключевые слова из VALID_KEYWORDS_1:", found_1)
    print("Найденные ключевые слова из VALID_KEYWORDS_2:", found_2)

    return bool(found_1 or found_2)


@load_router.callback_query(F.data == "load_report")
async def start_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("\U0001F4CE Загрузите ваш отчет в формате Excel (.xls или .xlsx).")
    await state.set_state(ReportStates.waiting_for_file)


@load_router.message(ReportStates.waiting_for_file, F.document)
async def process_file_upload(msg: Message, state: FSMContext):
    file_id = msg.document.file_id
    file_path = await bot.get_file(file_id)

    os.makedirs("temp", exist_ok=True)
    file_name = f"temp/{msg.document.file_name}"

    await bot.download_file(file_path.file_path, file_name)

    try:
        df = pd.read_excel(file_name, dtype=str, header=None)  # Загружаем без заголовков

        header_row = find_header_row(df)
        if header_row is None:
            await msg.answer("❌ Ошибка! Не удалось найти заголовки в файле. Проверьте его структуру.")
            return

        df.columns = df.iloc[header_row]  # Используем найденную строку как заголовки
        df = df.iloc[header_row + 1:].reset_index(drop=True)  # Убираем все строки выше

        print("Формат колонок после загрузки:", df.columns.tolist())  # Логирование заголовков
        print("Первые строки таблицы:\n", df.head(5))

        if contains_valid_keywords(df):
            await state.update_data(file_id=file_id)
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Да", callback_data="add_extra_expenses")],
                    [InlineKeyboardButton(text="Нет", callback_data="skip_extra_expenses")]
                ]
            )
            await msg.answer(
                "В отчете из маркетплейса не отображены некоторые виды расходов (например, зарплаты, аренда "
                "склада, реклама вне маркетплейса, связь/интернет, сервисы и прочее). Хотите ли вы их добавить?",
                reply_markup=keyboard)
            await state.set_state(ReportStates.asking_extra_expenses)
        else:
            await msg.answer("❌ Ошибка! Файл не содержит нужные данные. Проверьте структуру файла.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка обработки файла: {str(e)}\nУбедитесь, что это корректный .xls или .xlsx.")


@load_router.callback_query(F.data == "add_extra_expenses")
async def add_extra_expenses(callback: CallbackQuery, state: FSMContext):
    await state.update_data(expenses={}, current_category=list(EXPENSE_CATEGORIES.keys())[0])
    await callback.message.answer(
        f"Введите сумму для {EXPENSE_CATEGORIES[list(EXPENSE_CATEGORIES.keys())[0]]}.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]
        )
    )
    await state.set_state(ReportStates.entering_amount)


@load_router.callback_query(F.data == "skip_extra_expenses")
async def skip_extra_expenses(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file_id = data.get("file_id")
    user_id = callback.from_user.id
    async with async_session() as session:
        new_order = Order(user_id=user_id)
        session.add(new_order)
        await session.flush()
        new_expense = Expense(
            user_id=user_id,
            order_id=new_order.id,
            **{key: 0 for key in EXPENSE_CATEGORIES}
        )
        session.add(new_expense)
        await session.commit()

    await callback.message.answer("✅ Ваши расходы сохранены! Ожидайте ответа в течении 72 часов",
                                  reply_markup=main_kb)
    await notify_admins(new_order.id, file_id, {}, bot)  # уведомление админам
    await state.clear()


@load_router.callback_query(F.data == "skip_amount")
async def skip_amount(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_category = data.get("current_category")
    expenses = data.get("expenses", {})
    expenses[current_category] = 0
    await state.update_data(expenses=expenses)
    await ask_next_category(callback.message, state)


@load_router.message(ReportStates.entering_amount, F.text)
async def enter_amount(msg: Message, state: FSMContext):
    data = await state.get_data()
    current_category = data.get("current_category")
    expenses = data.get("expenses", {})

    if msg.text.isdigit():
        expenses[current_category] = int(msg.text)
    else:
        await msg.answer("Введите число или нажмите 'Пропустить'.")
        return

    await state.update_data(expenses=expenses)
    await ask_next_category(msg, state)


async def ask_next_category(msg, state: FSMContext):
    data = await state.get_data()
    expenses = data.get("expenses", {})
    remaining_categories = [cat for cat in EXPENSE_CATEGORIES if cat not in expenses]

    if remaining_categories:
        next_category = remaining_categories[0]
        await state.update_data(current_category=next_category)
        await msg.answer(
            f"Введите сумму для {EXPENSE_CATEGORIES[next_category]}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]
            )
        )
    else:
        summary = "\n".join([f"{EXPENSE_CATEGORIES[cat]}: {amount}" for cat, amount in expenses.items()])
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_expenses")],
                [InlineKeyboardButton(text="Ввести заново", callback_data="restart_expenses")]
            ]
        )
        await msg.answer(f"Ваши расходы:\n{summary}", reply_markup=keyboard)
        await state.set_state(ReportStates.confirmation)


@load_router.callback_query(F.data == "restart_expenses")
async def restart_expenses(callback: CallbackQuery, state: FSMContext):
    await state.update_data(expenses={}, current_category=list(EXPENSE_CATEGORIES.keys())[0])
    await callback.message.answer(
        f"Введите сумму для {EXPENSE_CATEGORIES[list(EXPENSE_CATEGORIES.keys())[0]]}.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]
        )
    )
    await state.set_state(ReportStates.entering_amount)


@load_router.callback_query(F.data == "confirm_expenses")
async def confirm_expenses(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    expenses = data.get("expenses", {})
    file_id = data.get("file_id")
    user_id = callback.from_user.id
    async with async_session() as session:
        new_order = Order(user_id=user_id)
        session.add(new_order)
        await session.flush()
        new_expense = Expense(
            user_id=user_id,
            order_id=new_order.id,
            **{key: expenses.get(key, 0) for key in EXPENSE_CATEGORIES}
        )
        session.add(new_expense)
        await session.commit()

    await callback.message.answer("✅ Ваши расходы сохранены! Ожидайте ответа в течении 72 часов",
                                  reply_markup=main_kb)
    await notify_admins(new_order.id, file_id, expenses, bot)
    await state.clear()
