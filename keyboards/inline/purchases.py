from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Оплатил",
                                 callback_data="paid")
        ],
        [
            InlineKeyboardButton(text="Отмена",
                                 callback_data="cancel")
        ],
    ]
)
