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
    ARSHIN_GREETING,
    GET_MI_MESSAGE,
    GET_MI_ERROR_MESSAGE,
    GET_INN_MESSAGE,
    GET_MIT_MESSAGE,
    GET_INN_ERROR_MESSAGE,
    GET_PHONE_ERROR_MESSAGE,
    NO_RESULTS_MESSAGE,
    GET_MIT_ERROR_MESSAGE,
)

router = Router()


@router.message(UserDoesntExist(UserType.ARSHIN), CommandStart())
async def new_user_start_handler(message: Message, state: FSMContext):
    await message.answer_photo(
        photo=FSInputFile(join_path("media", "number_hint.jpg")),
        caption=ARSHIN_GREETING,
        reply_markup=GET_NUMBER_KEYBOARD,
    )
    await state.set_state(UserHandelingStates.get_phone)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Добрый день!\nДля начала работы пришлите мне номер СИ!")
    await state.set_state(UserHandelingStates.get_mi)


@router.message(UserHandelingStates.get_phone, UserDoesntExist(UserType.ARSHIN))
async def get_phone_state_handler(message: Message, state: FSMContext):
    if hasattr(message, "contact"):
        await state.set_data({"phone": message.contact.phone_number})
        await message.answer(GET_INN_MESSAGE, reply_markup=None)
        await state.set_state(UserHandelingStates.get_inn)
        return

    await message.answer(GET_PHONE_ERROR_MESSAGE, reply_markup=GET_NUMBER_KEYBOARD)


@router.message(UserHandelingStates.get_inn, UserDoesntExist(UserType.ARSHIN))
async def get_inn_handler(message: Message, state: FSMContext):
    if message.text.isnumeric() and (
        len(message.text) == 10 or len(message.text) == 12
    ):
        await new_user(
            message.from_user, (await state.get_data())["phone"], message.text
        )
        await message.answer(GET_MI_MESSAGE)
        await state.set_state(UserHandelingStates.get_mi)

    else:
        await message.answer(GET_INN_ERROR_MESSAGE)


@router.message(UserHandelingStates.get_mi)
async def get_mit_handler(message: Message, state: FSMContext):
    await state.set_data({"mi": message.text})
    await message.answer(GET_MI_MESSAGE)
    await state.set_state(UserHandelingStates.get_mit)


@router.message(UserHandelingStates.get_mit)
async def get_mi_state_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    result, vri_id = await search(mi=message.text, mit=state_data["mi"])
    if result is None:
        await message.answer(
            NO_RESULTS_MESSAGE
            + "\n\n"
            + GET_MIT_ERROR_MESSAGE
            + "\n\n"
            + GET_MI_ERROR_MESSAGE
            + "\n\n"
            + GET_MI_MESSAGE
        )
        await state.set_state(UserHandelingStates.get_mi)
        return

    mit_title = f'{result["miInfo"]["singleMI"]["mitypeTitle"]} {result["miInfo"]["singleMI"]["mitypeType"]},\
        {result["miInfo"]["singleMI"]["modification"]}, {result["miInfo"]["singleMI"]["mitypeNumber"]}'
    await new_request(
        mi=state_data["mi"],
        tg_id=message.from_user.id,
        mit=message.text,
        mit_title=mit_title,
    )

    if "applicable" not in result["vriInfo"].keys():
        await message.answer(text="Свидетельство найдено, но не является применимым(")
        return

    await message.answer_document(
        FSInputFile(await create_document(result, vri_id, False, False)),
        caption="Свидетельство найдено!\nДля нового запроса просто новый номер СИ!\nВаш документ:",
    )
    await state.clear()
    await state.set_state(UserHandelingStates.get_mi)
