from sqlalchemy.future import select
from app.database.database import async_session
from app.database.models import Order


async def get_unprocessed_orders():
    async with async_session() as session:
        orders = await session.execute(select(Order.id).where(Order.processed == False))
        order_ids = [order[0] for order in orders.fetchall()]
    return order_ids
