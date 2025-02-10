from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Message


async def get_text(session: AsyncSession, name: str) -> str:
    """Извлекает текст сообщения по его названию."""
    message = await session.scalar(select(Message).where(Message.name == name))
    return message.content if message else "❌ Сообщение не найдено."
