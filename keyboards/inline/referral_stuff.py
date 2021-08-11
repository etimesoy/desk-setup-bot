from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_data import bot_functionality

referral_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Ввести ID пригласившего",
                             callback_data=bot_functionality.new("enter_referrer_id"))
    ],
    [
        InlineKeyboardButton(text="Подписаться на канал Desk Setup channel",
                             url="https://t.me/desk_setup_channel")
    ],
    [
        InlineKeyboardButton(text="Проверить подписку на канал",
                             callback_data=bot_functionality.new("check_channel_subscription"))
    ]
])

referral_system = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Создать пригласительную ссылку",
                             callback_data=bot_functionality.new("create_referral_link"))
    ]
])
