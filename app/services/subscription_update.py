from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from app.database.models import Subscription


async def update_subscription_status(user_id: int, session: AsyncSession, days: int = 30):
    """Обновляет или создаёт подписку для пользователя после оплаты."""

    # Ищем текущую подписку
    result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
    subscription = result.scalars().first()

    new_expiry = datetime.utcnow() + timedelta(days=days)  # Добавляем дни

    if subscription:
        # Обновляем подписку
        subscription.status = True
        subscription.expires_at = new_expiry
    else:
        # Создаём подписку
        subscription = Subscription(user_id=user_id, status=True, expires_at=new_expiry)
        session.add(subscription)

    await session.commit()
