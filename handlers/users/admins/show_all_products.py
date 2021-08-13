from aiogram import types

from keyboards.inline.callback_data import bot_functionality
from loader import dp, db


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_all_products"))
async def show_all_products(call: types.CallbackQuery):
    products = await db.select_all_products()
    message_text = "Все товары:\n"
    for product in products:
        message_text += f"{product['id']}) {product['name']}, {product['price']}₽. " \
                        f"{product['description']} link-{product['photo_link']}"
    await call.message.answer(message_text)
