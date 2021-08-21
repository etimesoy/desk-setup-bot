from typing import List

from aiogram import types

from keyboards.inline.callback_data import inline_mode_product
from loader import db


async def get_inline_results_for_query(chat_type: str, query: str = "") -> List[types.InlineQueryResultArticle]:
    products = await db.select_all_products()
    inline_query_results = []
    for product in sorted(products, key=lambda x: x["name"]):
        if product["name"].startswith(query):
            if chat_type == "sender":
                show_product_button = types.InlineKeyboardButton(
                    "Показать товар",
                    callback_data=inline_mode_product.new(product["id"], "show")
                )
            else:
                show_product_button = types.InlineKeyboardButton(
                    "Показать товар",
                    url=f"https://t.me/desk_setup_bot?start=show_product-{product['id']}"
                )
            inline_query_result = types.InlineQueryResultArticle(
                id=product["id"],
                thumb_url=product["photo_link"],
                title=product["name"] + " - " + str(product["price"]) + '₽',
                input_message_content=types.InputTextMessageContent(
                    product["name"] + " - " + str(product["price"]) + '₽' +
                    '\n' + f"<a href='{product['photo_link']}'>thumbnail</a>",
                ),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[show_product_button]])
            )
            inline_query_results.append(inline_query_result)
    return inline_query_results
