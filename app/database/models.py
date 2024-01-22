from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.types import BigInteger, String, DateTime, Integer
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, func
from typing import Optional, List


class AsyncTable(DeclarativeBase, AsyncAttrs):
    pass


class User(AsyncTable):
    __tablename__ = "fgis_bot_users"

    id: Mapped[int] = mapped_column(primary_key=True)

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, index=True, unique=True)
    username: Mapped[Optional[String]] = mapped_column(String, nullable=True)

    first_name: Mapped[String] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[String]] = mapped_column(String, nullable=True)
    phone: Mapped[String] = mapped_column(String, nullable=False)
    requests: Mapped[Optional[List["Requests"]]] = relationship(
        "Requests", back_populates="user"
    )

    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    @classmethod
    async def from_tg_user(cls, tg_user: TgUser, phone: str):
        return User(
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            phone=phone,
        )


class Requests(AsyncTable):
    __tablename__ = "fgis_bot_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    mit: Mapped[Optional[int]]
    mi: Mapped[Optional[int]]
    requested_by: Mapped[int] = mapped_column(ForeignKey("fgis_bot_users.id"))
    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    user = relationship("User")
