from aiogram.fsm.state import StatesGroup, State


class Avatar(StatesGroup):
    gender = State()
    age = State()
    hair = State()
