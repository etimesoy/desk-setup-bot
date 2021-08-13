from aiogram import types

from keyboards.inline.admins import admin_abilities
from keyboards.inline.callback_data import bot_functionality
from loader import dp


@dp.callback_query_handler(bot_functionality.filter(functionality_name="answer_admin_panel"))
@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_admin_panel"))
async def show_admin_panel(call: types.CallbackQuery, callback_data: dict):
    if callback_data['functionality_name'] == 'show_admin_panel':
        await call.message.edit_text("Админка:")
        await call.message.edit_reply_markup(admin_abilities)
    else:
        await call.message.answer("Админка:", reply_markup=admin_abilities)
