from aiogram import Router, F
from aiogram.filters import CommandStart, BaseFilter
from aiogram.types import (
    CallbackQuery,
    User,
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import app.database.requests as db
from app.web import search


class UserHandling(StatesGroup):
    get_phone = State()
    choose_bot_type = State()
    waiting_for_mi_input = State()
    waiting_for_mit_input = State()
    return_to_start = State()


class UserDoesntExistsFilter(BaseFilter):
    async def __call__(self, message: Message):
        return not await db.user_exists(message.from_user.id)


router = Router()


@router.message(CommandStart(), UserDoesntExistsFilter())
async def start_command_handler(message: Message, state: FSMContext):
    await state.set_state(UserHandling.get_phone)
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await message.answer("<Приветствие>", reply_markup=markup)


@router.message(UserHandling.get_phone)
async def get_phone_handler(message: Message, state: FSMContext):
    await db.new_user(message.from_user, message.contact.phone_number)
    await state.set_state(UserHandling.choose_bot_type)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="А")],
            [KeyboardButton(text="Б")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    await message.answer("Выберите тип бота.", reply_markup=markup)


@router.message(UserHandling.choose_bot_type)
async def get_bot_type(message: Message, state: FSMContext):
    match message.text.lower():
        case "а":
            await state.set_state(UserHandling.waiting_for_factory_number_input)
            await state.set_data({"type": "A"})
            await message.answer("Заводской номер / Буквенно-цифровое обозначение:")
        case "б":
            await state.set_state(UserHandling.waiting_for_mit_input)
            await state.set_data({"type": "B"})
            await message.answer("Регистрационный номер типа СИ:")


@router.message(UserHandling.waiting_for_mit_input)
async def get_mit_input(message: Message, state: FSMContext):
    if len(message.text) == 7 or (len(message.text) == 6 and "-" not in message.text):
        data = await state.get_data()
        data["mit_number"] = message.text
        await state.set_data(data)
        await state.set_state(UserHandling.waiting_for_mi_input)
        return
    await message.answer("Неправильный ввод!")

@router.message(UserHandling.waiting_for_mi_input)
async def get_mi_input(message: Message, state: FSMContext):
    if len(message.text) == 12 or (len(message.text) == 10 and " " not in message.text):
        data = await state.get_data()
        data["mi_number"] = message.text
        await state.set_state(UserHandling.return_to_start)
        await message.answer(str(await search(data["mi_number"], data["mit_number"])))
        return
    await message.answer("Некорректный ввод")