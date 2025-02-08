from app.database.database import async_session
from app.database.models import Price, Message
from sqlalchemy.future import select


from app.settings.logger_config import get_logger
logger = get_logger(__name__)


async def initialize_data():
    """Инициализация данных в БД (добавляет только если таблицы пустые)."""
    async with async_session() as session:
        # Проверяем, есть ли уже записи в Price
        result = await session.execute(select(Price))
        if not result.scalars().first():
            session.add_all([
                Price(subscription=5000, consultation=4150)
            ])
            logger.info("Добавлены начальные цены.")

        # Проверяем, есть ли уже записи в Message
        result = await session.execute(select(Message))
        if not result.scalars().first():
            session.add_all([
                Message(name="start", content="Здравствуйте! Этот бот формирует финансовую отчётность..."),
                Message(name="load_report", content="Загрузите отчет...")
            ])
            logger.info("Добавлены стандартные сообщения.")

        await session.commit()
