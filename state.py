from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateAd(StatesGroup):
    text = State()
    image = State()
    send = State()
