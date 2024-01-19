from aiogram import Router, F
from aiogram.filters import CommandStart, BaseFilter
from aiogram.types import CallbackQuery, User, Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import app.database.requests as db


class UserHandling(StatesGroup):
    get_phone = State()
    choose_bot_type = State()
    waiting_for_factory_number_input = State()
    waiting_for_mit_input = State()


class UserDoesntExistsFilter(BaseFilter):
    async def __call__(self, message: Message):
        return not await db.user_exists(message.from_user.id)


router = Router()


@router.message(CommandStart(), UserDoesntExistsFilter())
async def start_command_handler(message: Message, state: FSMContext):
    await state.set_state(UserHandling.get_phone)
    markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Поделиться контактом", request_contact=True)
        ]
    ], resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
    await message.answer("<Приветствие>", reply_markup=markup)


@router.message(UserHandling.get_phone)
async def get_phone_handler(message: Message, state: FSMContext):
    await db.new_user(message.from_user, message.contact.phone_number)
    await state.set_state(UserHandling.choose_bot_type)
