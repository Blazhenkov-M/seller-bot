from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from app.database.models import Subscription


async def update_subscription_status(user_id: int, session: AsyncSession, days: int = 30):
    """Обновляет или создаёт подписку для пользователя после оплаты."""
    async with session.begin():  # Безопасный контекстный менеджер для транзакции
        result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
        subscription = result.scalars().first()

        now = datetime.utcnow()

        if subscription:
            # Если подписка уже активна и срок не истёк, добавляем дни к expires_at
            if subscription.expires_at and subscription.expires_at > now:
                subscription.expires_at += timedelta(days=days)
            else:
                subscription.expires_at = now + timedelta(days=days)
            subscription.status = True
        else:
            # Создаём новую подписку
            subscription = Subscription(user_id=user_id, status=True, expires_at=now + timedelta(days=days))
            session.add(subscription)
