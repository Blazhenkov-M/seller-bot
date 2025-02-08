from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
# from app.services.get_admins import get_admins  # Функция для получения админов из БД

SUPER_ADMINS = {235886164, 5571245352}  # Фиксированные суперадмины


# class AdminProtect(BaseFilter):
#     def __init__(self, role: str = "admin"):  # "admin" или "superadmin"
#         self.role = role
#
#     async def __call__(self, event: Message | CallbackQuery) -> bool:
#         user_id = event.from_user.id
#
#         # Проверяем суперадминов и сразу возвращаем True
#         if user_id in SUPER_ADMINS:
#             return True
#
#         # Если роль требует именно суперадмина, а его нет — False
#         if self.role == "superadmin":
#             return False
#
#         # Для обычных админов запрашиваем из БД
#         db_admins = await get_admins()  # Здесь будет ошибка, если нет импорта
#         return user_id in db_admins
