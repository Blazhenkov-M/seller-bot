from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Price


async def get_consult_price(session: AsyncSession):
    """Получает цену консультации из базы данных (вторую запись)."""
    result = await session.execute(select(Price).limit(1))  # Берем первую запись
    price = result.scalars().first()

    return price.consultation if price else None
