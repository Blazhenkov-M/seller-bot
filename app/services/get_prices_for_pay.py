from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import Price


async def get_prices_for_pay(session: AsyncSession):
    """Получает цены подписки и консультации из базы данных."""
    result = await session.execute(select(Price).limit(1))  # Берем первую запись
    price = result.scalars().first()

    if price:
        return price.subscription, price.consultation
    return None, None  # Если в БД нет цен
