from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models import Admin, User
from app.settings.logger_config import get_logger

logger = get_logger(__name__)


async def get_admins():
    print('s')
