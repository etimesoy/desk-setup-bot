from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from keyboards.inline.callback_data import bot_functionality


def get_bot_functionality(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if str(user_id) in ADMINS:
        admin_button = InlineKeyboardButton(text="Перейти в админку",
                                            callback_data=bot_functionality.new("show_admin_panel"))
        keyboard.insert(admin_button)
    referral_system_button = InlineKeyboardButton(text="Реферальная система",
                                                  callback_data=bot_functionality.new("show_referral_system"))
    keyboard.insert(referral_system_button)
    choose_product_button = InlineKeyboardButton(text="Выбрать товар",
                                                 switch_inline_query_current_chat="")
    keyboard.insert(choose_product_button)
    return keyboard
