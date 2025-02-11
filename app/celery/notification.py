from datetime import datetime, timedelta
from celery import Celery
from app.database.database import AsyncSession
from app.database.models import User
from app.core.bot_instance import bot
from app.keyboards.user import get_pay_kb

celery = Celery("tasks", broker="redis://localhost:6379/1")


@celery.task
def notify_users_about_subscription():
    with AsyncSession() as session:
        threshold_date = datetime.utcnow() + timedelta(days=3)
        users = session.query(User).filter(User.subscription_expiry == threshold_date).all()

        for user in users:
            bot.send_message(user.tg_id, "Ваша подписка заканчивается через 3 дня\n\n"
                                         "Нажмите кнопку «Оплатить», чтобы подлить подписку 👇🏻",
                             reply_markup=get_pay_kb)
