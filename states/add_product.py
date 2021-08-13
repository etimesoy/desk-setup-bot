from aiogram.dispatcher.filters.state import StatesGroup, State


class AddProduct(StatesGroup):
    enter_name = State()
    enter_photo = State()
    enter_price = State()
    enter_description = State()
