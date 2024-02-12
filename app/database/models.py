from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.types import BigInteger, String, DateTime, Integer
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, func
from typing import Optional, List


class AsyncTable(DeclarativeBase, AsyncAttrs):
    pass


class ArshinUser(AsyncTable):
    __tablename__ = "fgis_arshin_bot_users"

    id: Mapped[int] = mapped_column(primary_key=True)

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, index=True, unique=True)
    username: Mapped[Optional[String]] = mapped_column(String, nullable=True)

    first_name: Mapped[String] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[String]] = mapped_column(String, nullable=True)
    phone: Mapped[String] = mapped_column(String, nullable=False)
    inn: Mapped[Optional[String]] = mapped_column(String, nullable=True)
    requests: Mapped[Optional[List["Requests"]]] = relationship(
        "Requests", back_populates="arshin_user"
    )

    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    @classmethod
    async def from_tg_user(cls, tg_user: TgUser, phone: str, inn: str):
        return ArshinUser(
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            phone=phone,
            inn=inn,
        )


class QuasarUser(AsyncTable):
    __tablename__ = "fgis_quasar_bot_users"

    id: Mapped[int] = mapped_column(primary_key=True)

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, index=True, unique=True)
    username: Mapped[Optional[String]] = mapped_column(String, nullable=True)

    first_name: Mapped[String] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[String]] = mapped_column(String, nullable=True)
    phone: Mapped[String] = mapped_column(String, nullable=False)
    requests: Mapped[Optional[List["Requests"]]] = relationship(
        "Requests", back_populates="quasar_user"
    )

    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    @classmethod
    async def from_tg_user(cls, tg_user: TgUser, phone: str):
        return QuasarUser(
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            phone=phone,
        )


class Requests(AsyncTable):
    __tablename__ = "fgis_bot_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    mit: Mapped[String] = mapped_column(String, nullable=True)
    mi: Mapped[String] = mapped_column(String, nullable=True)
    mit_title: Mapped[String] = mapped_column(String)
    requested_by_arshin: Mapped[Optional[int]] = mapped_column(
        ForeignKey("fgis_arshin_bot_users.tg_id")
    )
    requested_by_quasar: Mapped[Optional[int]] = mapped_column(
        ForeignKey("fgis_quasar_bot_users.tg_id")
    )
    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    arshin_user = relationship("ArshinUser")
    quasar_user = relationship("QuasarUser")
