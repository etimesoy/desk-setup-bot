from aiogram import types

from keyboards.inline.admins import admin_abilities
from keyboards.inline.callback_data import bot_functionality
from loader import dp


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_admin_panel"))
async def show_admin_panel(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer("Админка:", reply_markup=admin_abilities)
