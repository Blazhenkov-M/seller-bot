import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models import User, Subscription
from app.celery.notifications import notify_users_about_subscription


@pytest.fixture
async def mock_db_session(mocker):
    """Создает мок для асинхронной сессии БД."""
    mock_session = AsyncMock(spec=AsyncSession)

    test_user = User(tg_id=123456, username="test_user")
    test_subscription = Subscription(
        user_id=test_user.tg_id,
        status=True,
        expires_at=datetime.utcnow() + timedelta(days=3)
    )

    # Мок запроса к БД
    mock_session.execute.return_value.scalars.return_value.all.return_value = [test_user.tg_id]

    return mock_session


@pytest.mark.asyncio
async def test_notify_users_about_subscription(mocker, mock_db_session):
    """Тестирует уведомление о подписке."""
    mock_send_message = mocker.patch("app.core.bot_instance.bot.send_message", new_callable=AsyncMock)

    # Запускаем функцию с замоканной сессией
    await notify_users_about_subscription(mock_db_session)

    # Проверяем, что send_message вызван один раз с нужными аргументами
    mock_send_message.assert_called_once_with(
        123456,
        "Ваша подписка заканчивается через 3 дня!\n\n"
        "Нажмите кнопку «Оплатить», чтобы продлить подписку 👇🏻",
        reply_markup=mocker.ANY
    )
