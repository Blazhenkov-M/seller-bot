from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Numeric, Boolean, func, Text, Integer
from datetime import datetime
from app.database.database import Base


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    reg_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("Expense", back_populates="user")
    orders = relationship("Order", back_populates="user")
    admin = relationship("Admin", back_populates="user", uselist=False)
    subscription = relationship("Subscription", back_populates="user", uselist=False)  # Добавляем связь


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"), unique=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False)  # Активна или нет
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)  # Когда закончится подписка

    user = relationship("User", back_populates="subscription")


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete="CASCADE"), unique=True)

    user = relationship("User", back_populates="admin")


class Price(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscription: Mapped[int] = mapped_column(Integer, nullable=False)
    consultation: Mapped[int] = mapped_column(Integer, nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # Название сообщения
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Текст сообщения


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    processed: Mapped[bool] = mapped_column(Boolean, default=False)  # Обработан или нет

    user = relationship("User", back_populates="orders")
    expenses = relationship("Expense", back_populates="order")


class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete="CASCADE"))  # Привязка к заказу
    salaries: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    advertising: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    warehouse_rent: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    communication: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    services: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    other: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="expenses")
    order = relationship("Order", back_populates="expenses")
