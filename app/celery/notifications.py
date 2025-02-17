from datetime import datetime, timedelta
from sqlalchemy.future import select

from app.celery import celery
from app.database.database import async_session
from app.database.models import Subscription, User
from app.core.bot_instance import bot
from app.keyboards.user import get_pay_kb


@celery.task
async def notify_users_about_subscription():
    """Оповещает пользователей за 3 дня до окончания подписки."""
    async with async_session() as session:
        threshold_date = datetime.utcnow() + timedelta(days=3)

        result = await session.execute(
            select(User.tg_id)
            .join(Subscription)
            .where(Subscription.expires_at <= threshold_date, Subscription.status == True)
        )

        users = result.scalars().all()

        for tg_id in users:
            await bot.send_message(
                tg_id,
                "Ваша подписка заканчивается через 3 дня!\n\n"
                "Нажмите кнопку «Оплатить», чтобы продлить подписку 👇🏻",
                reply_markup=get_pay_kb
            )
