from app.filters.admin_protect import SUPER_ADMINS
from app.services.get_admins import get_admins
from app.core.expense_categories import EXPENSE_CATEGORIES


async def notify_admins(order_id: int, file_id: str, expenses: dict, bot):
    # Получаем список админов
    db_admins = await get_admins()
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
