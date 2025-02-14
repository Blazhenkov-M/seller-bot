from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message
from app.database.database import async_session
from app.database.models import Expense, Order
from app.core.bot_instance import bot
from app.services import get_admins

load_router = Router()

# Русские названия категорий
EXPENSE_CATEGORIES = {
    "salaries": "Зарплаты",
    "advertising": "Реклама вне маркетплейса",
    "warehouse_rent": "Аренда склада",
    "communication": "Связь/интернет",
    "services": "Сервисы (эквайринг/комиссии банка/ПО/CRM/программы)",
    "other": "Прочее"
}


class ReportStates(StatesGroup):
    waiting_for_file = State()
    entering_amount = State()
    confirmation = State()


@load_router.callback_query(F.data == "load_report")
async def start_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📎 Загрузите ваш отчет в формате Excel (.xls или .xlsx).")
    await state.set_state(ReportStates.waiting_for_file)


@load_router.message(ReportStates.waiting_for_file, F.document)
async def process_file_upload(msg: Message, state: FSMContext):
    file_id = msg.document.file_id
    await state.update_data(file_id=file_id, expenses={}, current_category=list(EXPENSE_CATEGORIES.keys())[0])
    await msg.answer(f"Введите сумму для {EXPENSE_CATEGORIES[list(EXPENSE_CATEGORIES.keys())[0]]}.",
                     reply_markup=InlineKeyboardMarkup(
                         inline_keyboard=[[InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]))
    await state.set_state(ReportStates.entering_amount)


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
        await msg.answer(f"Введите сумму для {EXPENSE_CATEGORIES[next_category]}",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[[InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]))
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
    await callback.message.answer(f"Введите сумму для {EXPENSE_CATEGORIES[list(EXPENSE_CATEGORIES.keys())[0]]}.",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [InlineKeyboardButton(text="Пропустить", callback_data="skip_amount")]]))
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

    await callback.message.answer("✅ Ваши расходы сохранены!")
    await notify_admins(new_order.id, file_id, expenses, bot)
    await state.clear()


SUPER_ADMINS = {235886164, 5571245352}  # Фиксированные суперадмины


async def notify_admins(order_id: int, file_id: str, expenses: dict, bot):
    # Получаем список админов
    db_admins = await get_admins.get_admins()
    all_admins = set(db_admins) | SUPER_ADMINS  # Объединяем с супер-админами

    # Формируем сообщение
    summary = "\n".join([f"{EXPENSE_CATEGORIES.get(cat, cat)}: {amount}" for cat, amount in expenses.items()])
    message_text = f"📊 Новый загруженный отчет\n🆔 Номер заказа: {order_id}\n💰 Расходы:\n{summary}"

    # Отправляем сообщение каждому админу
    for admin_id in all_admins:
        try:
            await bot.send_message(admin_id, message_text)
            await bot.send_document(admin_id, file_id)
        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin_id}: {e}")
