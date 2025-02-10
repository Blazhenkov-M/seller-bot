from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Price


async def get_prices(session: AsyncSession):
    """Получает текущие цены из базы данных."""
    result = await session.execute(select(Price))
    return result.scalars().first()  # Должна быть одна запись с ценами


async def update_price(session: AsyncSession, field: str, value: int):
    """Обновляет цену в базе данных."""
    price = await session.scalar(select(Price))

    if not price:
        price = Price(subscription=5000, consultation=4150)
        session.add(price)

    if field == "subscription":
        price.subscription = value
    elif field == "consultation":
        price.consultation = value

    await session.commit()
    return price
