from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.settings.config import settings


class Base(DeclarativeBase):
    __table_args__ = {'extend_existing': True}


engine = create_async_engine(url=settings.sqlalchemy_database_url,
                             echo=False,
                             future=True,
                             connect_args={"server_settings": {"timezone": "UTC"}},
                             pool_size=10,
                             max_overflow=10)

# Создаем сессию для работы с базой данных
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
