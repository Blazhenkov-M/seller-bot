from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.core.bot_instance import bot
from app.filters.admin_protect import AdminProtect
from sqlalchemy.future import select
from app.database.database import async_session
from app.database.models import Order, User
from app.services.get_orders import get_unprocessed_orders
from app.states import OrderResponse

admin_response = Router()


# Шаг 1: Запрос номера заказа
@admin_response.callback_query(AdminProtect("admin"), F.data == "response_user")
async def start_response(callback: CallbackQuery, state: FSMContext):
    order_ids = await get_unprocessed_orders()
    if order_ids:
        orders_list = ", ".join(map(str, order_ids))
        await callback.message.answer(f"Необработанные заказы: {orders_list}\nВведите номер заказа:")
        await state.set_state(OrderResponse.waiting_for_order_number)  # Устанавливаем состояние
    else:
        await callback.message.answer("Нет необработанных заказов.")

    await callback.answer()


# Шаг 2: Проверка номера заказа
@admin_response.message(OrderResponse.waiting_for_order_number)
async def check_order(message: Message, state: FSMContext):
    try:
        order_number = int(message.text.strip())  # Приводим к int
    except ValueError:
        await message.answer("Некорректный номер заказа. Введите число.")
        return

    async with async_session() as session:
        order = await session.execute(
            select(Order).where(Order.id == order_number, Order.processed == False)
        )
        order = order.scalars().first()

        if not order:
            await message.answer("Заказ не найден или уже обработан.")
            return

        await message.answer("Введите сообщение для пользователя с ссылкой.")

        # Сохраняем order_id в state
        await state.update_data(order_id=order.id)
        await state.set_state(OrderResponse.waiting_for_message)  # Устанавливаем следующее состояние


# Шаг 3: Ввод сообщения и отправка пользователю
@admin_response.message(OrderResponse.waiting_for_message)
async def send_response(message: Message, state: FSMContext):
    data = await state.get_data()
    order_id = data.get("order_id")

    if not order_id:
        await message.answer("Ошибка: не найден заказ. Начните сначала.")
        await state.clear()
        return

    async with async_session() as session:
        order = await session.get(Order, order_id)
        if not order or order.processed:
            await message.answer("Ошибка: заказ уже обработан или не найден.")
            await state.clear()
            return

        user = await session.get(User, order.user_id)
        if not user:
            await message.answer("Ошибка: пользователь не найден.")
            await state.clear()
            return

        # Отправляем сообщение пользователю
        await bot.send_message(user.tg_id, f"Ответ на ваш заказ {order.id}: {message.text}")

        # Обновляем статус заказа
        order.processed = True
        session.add(order)  # Добавляем объект перед коммитом
        await session.commit()

        await message.answer("Ответ отправлен, заказ помечен как обработанный.")

        # Очищаем состояние
        await state.clear()
