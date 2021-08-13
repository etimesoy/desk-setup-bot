import markup as markup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.admins import show_admin_panel
from keyboards.inline.callback_data import bot_functionality, add_product
from loader import dp, db
from states import AddProduct


@dp.callback_query_handler(add_product.filter(level="1"), state=AddProduct.enter_price)
@dp.callback_query_handler(add_product.filter(level="2"), state=AddProduct.enter_description)
async def navigate_back_button(call: types.CallbackQuery, callback_data: dict,
                               state: FSMContext):
    await call.message.delete()
    product_data = await state.get_data()

    levels = {
        "1": {
            "product_property": "name",
            "function": add_product_name
        },
        "2": {
            "product_property": "photo",
            "function": add_product_photo
        }
    }
    current_level = callback_data["level"]

    product_property = product_data.get(levels[current_level]["product_property"])
    await levels[current_level]["function"](call.message, state, product_property)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_admin_panel"),
                           state=AddProduct.enter_name)
async def back_to_admin_panel(call: types.CallbackQuery, callback_data: dict,
                              state: FSMContext):
    await state.reset_state()
    await show_admin_panel(call, callback_data)


@dp.callback_query_handler(add_product.filter(level="0"), state=AddProduct.enter_photo)
@dp.callback_query_handler(bot_functionality.filter(functionality_name="add_product"))
async def add_product_start(call: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        "Назад в админку",
        callback_data=bot_functionality.new("show_admin_panel")
    )]])
    await call.message.edit_text("Введите название", reply_markup=markup)
    await AddProduct.enter_name.set()


@dp.message_handler(state=AddProduct.enter_name)
async def add_product_name(message_or_call: types.Message, state: FSMContext,
                           product_name: str = None):
    if product_name is None:
        product_name = message_or_call.text
    await state.update_data(name=product_name)

    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=add_product.new(
            level=CURRENT_LEVEL - 1
        ))
    ]])

    await message_or_call.answer("Введите ссылку на фотографию", reply_markup=markup)
    await AddProduct.enter_photo.set()


@dp.message_handler(state=AddProduct.enter_photo)
async def add_product_photo(message: types.Message, state: FSMContext,
                            product_photo: str = None):
    if product_photo is None:
        product_photo = message.text
    await state.update_data(photo=product_photo)

    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=add_product.new(
            level=CURRENT_LEVEL - 1
        ))
    ]])

    await message.answer("Введите цену", reply_markup=markup)
    await AddProduct.enter_price.set()


@dp.message_handler(state=AddProduct.enter_price)
async def add_product_price(message: types.Message, state: FSMContext):
    product_price = message.text
    await state.update_data(price=product_price)

    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=add_product.new(
            level=CURRENT_LEVEL - 1
        ))
    ]])

    await message.answer("Введите описание", reply_markup=markup)
    await AddProduct.enter_description.set()


@dp.message_handler(state=AddProduct.enter_description)
async def add_product_description(message: types.Message, state: FSMContext):
    product_description = message.text
    await state.update_data(description=product_description)

    product = await state.get_data()

    message_text = '\n'.join(["Вы добавили товар:",
                              f"Название: {product['name']}",
                              f"Фотография: {product['photo']}",
                              f"Цена: {product['price']}",
                              f"Описание: {product['description']}"])
    await db.add_product(product['name'], product['photo'], int(product['price']), product['description'])

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Главное меню", callback_data=bot_functionality.new("answer_menu")),
        InlineKeyboardButton("Админка", callback_data=bot_functionality.new("answer_admin_panel"))
    ]])

    await message.answer(message_text, reply_markup=markup)
    await state.reset_state()
