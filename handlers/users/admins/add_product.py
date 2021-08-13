from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import bot_functionality, add_product
from loader import dp
from states import AddProduct


@dp.callback_query_handler(add_product.filter(level="0"), state=AddProduct.enter_photo)
@dp.callback_query_handler(bot_functionality.filter(functionality_name="add_product"))
async def add_product_start(call: types.CallbackQuery):
    await call.message.answer("Введите название")
    await AddProduct.enter_name.set()


@dp.callback_query_handler(add_product.filter(level="1"), state=AddProduct.enter_price)
@dp.message_handler(state=AddProduct.enter_name)
async def add_product_name(message_or_call: Union[types.Message, types.CallbackQuery], state: FSMContext):
    product_data = await state.get_data()
    if isinstance(message_or_call, types.Message):
        product_name = message_or_call.text
    else:
        product_name = product_data.get("name")
    await state.update_data(name=product_name)

    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=add_product.new(
            level=CURRENT_LEVEL - 1
        ))
    ]])

    if isinstance(message_or_call, types.Message):
        await message_or_call.answer("Введите ссылку на фотографию", reply_markup=markup)
    else:
        await message_or_call.message.answer("Введите ссылку на фотографию", reply_markup=markup)
    await AddProduct.enter_photo.set()


@dp.callback_query_handler(add_product.filter(level="2"), state=AddProduct.enter_description)
@dp.message_handler(state=AddProduct.enter_photo)
async def add_product_photo(message_or_call: Union[types.Message, types.CallbackQuery], state: FSMContext):
    product_data = await state.get_data()
    if isinstance(message_or_call, types.Message):
        product_photo = message_or_call.text
    else:
        product_photo = product_data.get("photo")
    await state.update_data(photo=product_photo)

    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=add_product.new(
            level=CURRENT_LEVEL - 1
        ))
    ]])

    if isinstance(message_or_call, types.Message):
        await message_or_call.answer("Введите цену", reply_markup=markup)
    else:
        await message_or_call.message.answer("Введите цену", reply_markup=markup)
    await AddProduct.enter_price.set()


# @dp.callback_query_handler(add_product.filter(level="3"))
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

    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Главное меню", callback_data=bot_functionality.new("answer_menu")),
        InlineKeyboardButton("Админка", callback_data=bot_functionality.new("answer_admin_panel"))
    ]])

    await message.answer(message_text, reply_markup=markup)
    await state.reset_state()