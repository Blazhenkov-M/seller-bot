from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models import Admin, User
from app.settings.logger_config import get_logger

logger = get_logger(__name__)


async def get_admins_list(session: AsyncSession):
    """Получает список админов и их никнеймы."""
    try:
        result = await session.scalars(
            select(User.username).join(Admin, User.tg_id == Admin.user_id)
        )
        admins = [username for username in result if username]

        if not admins:
            return None

        return admins

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка админов: {e}")
        return None


async def add_admin(username: str, session: AsyncSession) -> bool:
    """Добавляет пользователя в список админов, если он есть в users."""
    try:
        # Ищем пользователя по username
        user = await session.scalar(select(User).where(User.username == username))

        if not user:
            return False  # Если юзер не найден, возвращаем False

        # Проверяем, не является ли он уже админом
        existing_admin = await session.scalar(select(Admin).where(Admin.user_id == user.tg_id))

        if existing_admin:
            return None  # Если уже админ, возвращаем None

        # Добавляем в админы
        new_admin = Admin(user_id=user.tg_id)
        session.add(new_admin)
        await session.commit()
        logger.info(f"User {username} назначен администратором")

        return True

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка при добавлении администратора {username}: {e}")
        return False


async def remove_admin(username: str, session: AsyncSession) -> bool:
    """Удаляет пользователя из списка админов, если он есть в таблице admins."""
    try:
        # Ищем пользователя по username
        user = await session.scalar(select(User).where(User.username == username))

        if not user:
            return False  # Если юзер не найден, возвращаем False

        # Ищем запись в admins
        admin = await session.scalar(select(Admin).where(Admin.user_id == user.tg_id))

        if not admin:
            return None  # Если он не админ, возвращаем None

        # Удаляем админа
        await session.delete(admin)
        await session.commit()
        logger.info(f"Пользователь @{username} удален из администраторов")

        return True

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка при удалении администратора {username}: {e}")
        return False
