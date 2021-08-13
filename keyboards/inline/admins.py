from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import bot_functionality

admin_abilities = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Все товары",
                             callback_data=bot_functionality.new("show_all_products")),
        InlineKeyboardButton(text="Добавить товар",
                             callback_data=bot_functionality.new("add_product"))
    ],
    [
        InlineKeyboardButton(text="Пользователи",
                             callback_data=bot_functionality.new("show_users"))
    ]
])
