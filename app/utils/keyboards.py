from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


GET_NUMBER_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Подвердить номер",
                request_contact=True,
            )
        ]
    ],
    is_persistent=True,
    resize_keyboard=True,
    one_time_keyboard=True,
)
