from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User


async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()
