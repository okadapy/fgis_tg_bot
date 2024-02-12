from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import ArshinUser, Requests, QuasarUser, AsyncTable
from sqlalchemy import select
from aiogram.types import User as TgUser
from config import DB_URL

_engine = create_async_engine(DB_URL, echo=True)
_sessionmaker = async_sessionmaker(_engine)


async def create_tables():
    async with _engine.begin() as con:
        await con.run_sync(AsyncTable.metadata.create_all)


async def quasar_user_exists(id: int) -> bool:
    async with _sessionmaker() as session:
        stmt = select(QuasarUser.id).where(QuasarUser.tg_id == id).limit(1)
        res = await session.execute(stmt)
        await session.commit()
    return any(res)


async def arshin_user_exists(id: int) -> bool:
    async with _sessionmaker() as session:
        stmt = select(ArshinUser.id).where(ArshinUser.tg_id == id).limit(1)
        res = await session.execute(stmt)
        await session.commit()
    return any(res)


async def new_user(user: TgUser, phone: str, inn: str | None = None):
    if inn is not None:
        new_user = await ArshinUser.from_tg_user(user, phone, inn)
    else:
        new_user = await QuasarUser.from_tg_user(user, phone)
    async with _sessionmaker() as session:
        session.add(new_user)
        await session.commit()


async def new_request(mi: str, tg_id: int, mit_title: str, mit: str | None = None):
    if mit is not None:
        new_request = Requests(
            mi=mi, mit=mit, requested_by_arshin=tg_id, mit_title=mit_title
        )
    else:
        new_request = Requests(
            mi=mi, requested_by_quasar=tg_id, mit=mit, mit_title=mit_title
        )
    async with _sessionmaker() as session:
        session.add(new_request)
        await session.commit()
