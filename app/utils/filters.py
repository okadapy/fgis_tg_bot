from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database.requests import quasar_user_exists, arshin_user_exists
from typing import Union
import enum


class UserType(enum.Enum):
    ARSHIN = 1
    QUASAR = 2


class UserDoesntExist(BaseFilter):
    def __init__(self, user_type: UserType) -> None:
        self.__usertype = user_type

    async def __call__(self, message: Message):
        if self.__usertype == UserType.ARSHIN:
            return not await arshin_user_exists(message.from_user.id)
        if self.__usertype == UserType.QUASAR:
            return not await quasar_user_exists(message.from_user.id)
