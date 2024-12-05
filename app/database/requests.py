from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, delete
from datetime import datetime, timedelta

async def set_user(tg_id, time):

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, time = datetime.utcnow() + timedelta(30*int(time))))
            await session.commit()

async def get_info(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(User).where(User.tg_id == tg_id))
        if data:
            remaining_time = (data.time - datetime.utcnow()).days
            return remaining_time

async def del_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.delete(user)
        await session.commit()
