from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models import User

from app.settings.logger_config import get_logger
logger = get_logger(__name__)


async def add_user(tg_id: int, username: str, session: AsyncSession):
    """Добавляет нового пользователя в базу данных или обновляет существующего."""
    try:
        # Проверяем, существует ли пользователь с таким tg_id
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            action = "created"
        else:
            user.username = username  # Если пользователь существует, обновляем его username
            action = "updated"

        await session.commit()
        logger.info(f"User {tg_id} {action} successfully")

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error adding/updating user {tg_id}: {e}")
        raise
