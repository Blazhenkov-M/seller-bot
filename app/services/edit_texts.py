from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Message


async def update_message_content(session: AsyncSession, name: str, new_content: str):
    """Обновляет контент сообщения в базе данных."""
    message = await session.scalar(select(Message).where(Message.name == name))

    if message:
        message.content = new_content
        await session.commit()
        return message
    return None
