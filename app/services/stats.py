from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Admin, Subscription, Order


async def get_all_usernames(session: AsyncSession) -> list[str]:
    """Получает список никнеймов пользователей, исключая админов."""

    # Получаем user_id всех админов
    admin_user_ids = await session.scalars(select(Admin.user_id))
    admin_user_ids = set(admin_user_ids)  # Делаем множество для быстрого поиска

    # Получаем пользователей, которых нет в списке админов
    users = await session.scalars(select(User.username).where(User.tg_id.not_in(admin_user_ids)))
    usernames = [f"@{username}" for username in users if username]  # Форматируем никнеймы
    return usernames


async def calculate_conversion(session: AsyncSession) -> str:
    # Количество пользователей, нажавших /start
    total_users = (await session.execute(select(func.count()).select_from(User))).scalar_one()

    # Количество оплативших подписку
    paid_users = (await session.execute(select(func.count()).select_from(Subscription).where(Subscription.status == True))).scalar_one()

    # Количество отправленных отчетов
    total_reports = (await session.execute(select(func.count()).select_from(Order))).scalar_one()

    # Количество обработанных отчетов
    processed_reports = (await session.execute(select(func.count()).select_from(Order).where(Order.processed == True))).scalar_one()

    # Рассчитываем проценты (избегаем деления на 0)
    paid_conversion = round((paid_users / total_users * 100) if total_users else 0, 2)
    report_conversion = round((total_reports / total_users * 100) if total_users else 0, 2)
    processed_conversion = round((processed_reports / total_users * 100) if total_users else 0, 2)

    return (
        f"📊 **Конверсия:**\n\n"
        f"👤 Всего пользователей: {total_users}\n"
        f"💳 Оплатили подписку: {paid_users} ({paid_conversion}%)\n"
        f"📤 Отправили отчет: {total_reports} ({report_conversion}%)\n"
        f"✅ Обработанные отчеты: {processed_reports} ({processed_conversion}%)"
    )
