from datetime import datetime
from app.database.database import AsyncSession
from app.database.models import User


def is_subscription_active(user_id: int) -> bool:
    with AsyncSession() as session:
        user = session.query(User).filter(User.tg_id == user_id).first()
        if user and user.subscription_expiry and user.subscription_expiry > datetime.utcnow():
            return True
        return False
