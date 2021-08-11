from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_abilities = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Пользователи", callback_data="show_users")
    ],
    [
        InlineKeyboardButton(text="Добавить товар", callback_data="add_product")
    ]
])
