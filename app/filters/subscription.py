from aiogram.filters import BaseFilter
from aiogram.types import Message


from app.services.subscription_active import is_subscription_active


class SubscriptionRequired(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return is_subscription_active(message.from_user.id)
