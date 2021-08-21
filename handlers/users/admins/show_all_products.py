from aiogram import types

from keyboards.inline.callback_data import bot_functionality
from loader import dp, db


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_all_products"))
async def show_all_products(call: types.CallbackQuery):
    products = await db.select_all_products()
    message_text = "Все товары:"
    for product in products:
        product_photo_link = product["photo_link"]
        message_text += f"\n{product['id']}) {product['name']}, {product['price']}₽. " \
                        f"{product['description']} <a href='{product['photo_link']}'>link</a>"
    await call.message.answer(message_text, disable_web_page_preview=True)
