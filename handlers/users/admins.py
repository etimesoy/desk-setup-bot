from aiogram import types

from keyboards.inline.admins import admin_abilities
from keyboards.inline.callback_data import bot_functionality
from loader import dp, db, bot


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_admin_panel"))
async def show_admin_panel(call: types.CallbackQuery):
    await call.message.edit_text("Админка:")
    await call.message.edit_reply_markup(admin_abilities)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_users"))
async def show_users(call: types.CallbackQuery):
    users = await db.select_all_users()
    message_text = "Пользователи, зарегистированные в боте:\n"
    for user in users:
        message_text += f"{user['id']}) {user['full_name']} (@{user['username']}), был приглашен "
        referrer_id = user['referrer_id']
        if referrer_id == "-1001594274069":
            message_text += "из канала"
        else:
            referrer = await bot.get_chat_member(referrer_id, referrer_id)
            referrer_username = referrer['user']['username']
            message_text += f"юзером @{referrer_username}"
        message_text += "\n"
    await call.message.answer(message_text)
