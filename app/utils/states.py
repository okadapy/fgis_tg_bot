from aiogram.fsm.state import State, StatesGroup


class UserHandelingStates(StatesGroup):
    get_phone = State()
    get_inn = State()
    get_mi = State()
    get_mit = State()
