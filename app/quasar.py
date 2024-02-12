from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from app.utils.filters import UserDoesntExist, UserType
from os.path import join as join_path
from app.utils.keyboards import GET_NUMBER_KEYBOARD
from app.utils.states import UserHandelingStates
from app.database.requests import new_user, new_request
from app.utils.search import search
from app.utils.docx import create_document
from config import (
    QUASAR_GREETING,
    GET_MI_MESSAGE,
    GET_MI_ERROR_MESSAGE,
    GET_PHONE_ERROR_MESSAGE,
)

router = Router()


@router.message(UserDoesntExist(UserType.QUASAR), CommandStart())
async def new_user_start_handler(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile(join_path("media", "number_hint.jpg")),
        caption=QUASAR_GREETING,
        reply_markup=GET_NUMBER_KEYBOARD,
    )
    await state.set_state(UserHandelingStates.get_phone)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        "Добрый день!\nДля начала работы пришлите мне\n" + GET_MI_MESSAGE
    )
    await state.set_state(UserHandelingStates.get_mi)


@router.message(UserHandelingStates.get_phone)
async def get_phone_state_handler(message: Message, state: FSMContext):
    if hasattr(message, "contact"):
        await new_user(message.from_user, message.contact.phone_number)
        await message.answer(GET_MI_MESSAGE, reply_markup=None)
        await state.set_state(UserHandelingStates.get_mi)
    else:
        await message.answer(GET_PHONE_ERROR_MESSAGE, reply_markup=GET_NUMBER_KEYBOARD)


@router.message(UserHandelingStates.get_mi)
async def get_mi_state_handler(message: Message, state: FSMContext):
    result, vri_id = await search(message.text)
    if result is None:
        await message.answer(
            "Свидетельства о поверке не найдено!"
            + "\n\n"
            + GET_MI_ERROR_MESSAGE
            + "\n\n И"
            + GET_MI_MESSAGE.lower()
        )
        return

    mit_title = f'{result["miInfo"]["singleMI"]["mitypeTitle"]} {result["miInfo"]["singleMI"]["mitypeType"]},\
        {result["miInfo"]["singleMI"]["modification"]}, {result["miInfo"]["singleMI"]["mitypeNumber"]}'
    await new_request(mi=message.text, tg_id=message.from_user.id, mit_title=mit_title)
    await message.answer_document(
        FSInputFile(await create_document(result, vri_id, True)),
        caption="Свидетельство найдено!\nДля повторного запроса введите Заводской номер.\nВаш документ:",
    )
