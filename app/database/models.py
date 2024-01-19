from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.types import BigInteger, String, DateTime
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

    created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    requests: Mapped[List["Request"]] = relationship(back_populates="user")

class Request(AsyncTable):
    __tablename__ = "fgis_bot_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_type: Mapped[String] = mapped_column(String, nullable=False)
    mit_id: Mapped[int] = mapped_column(index=True, nullable=False)
    number: Mapped[int] = mapped_column(index=True, nullable=False)
    