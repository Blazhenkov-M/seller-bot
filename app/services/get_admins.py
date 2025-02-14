from sqlalchemy.future import select
from app.database.models import Admin
from app.database.database import async_session
from app.settings.logger_config import get_logger

logger = get_logger(__name__)


async def get_admins() -> list[int]:
    """Возвращает список Telegram ID администраторов."""
    async with async_session() as session:
        result = await session.execute(select(Admin.user_id))
        admins = result.scalars().all()
        return list(admins)
