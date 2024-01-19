from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import User, Requests, AsyncTable
from sqlalchemy import select
from aiogram.types import User as TgUser
from config import DB_URL

_engine = create_async_engine(DB_URL, echo=True)
_sessionmaker = async_sessionmaker(_engine)


async def create_tables():
    async with _engine.begin() as con:
        await con.run_sync(AsyncTable.metadata.create_all)


async def user_exists(id: int) -> bool:
    async with _sessionmaker() as session:
        stmt = select(User.id).where(User.tg_id == id).limit(1)
        res = await session.execute(stmt)
        await session.commit()
    return any(res)


async def new_user(user: TgUser, phone: str):
    new_user = await User.from_tg_user(user, phone)
    async with _sessionmaker() as session:
        session.add(new_user)
        await session.commit()
