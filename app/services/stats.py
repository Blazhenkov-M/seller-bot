from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Admin


async def get_all_usernames(session: AsyncSession) -> list[str]:
    """Получает список никнеймов пользователей, исключая админов."""

    # Получаем user_id всех админов
    admin_user_ids = await session.scalars(select(Admin.user_id))
    admin_user_ids = set(admin_user_ids)  # Делаем множество для быстрого поиска

    # Получаем пользователей, которых нет в списке админов
    users = await session.scalars(select(User.username).where(User.tg_id.not_in(admin_user_ids)))
    usernames = [f"@{username}" for username in users if username]  # Форматируем никнеймы
    return usernames
