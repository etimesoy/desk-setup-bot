from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from keyboards.inline.callback_data import bot_functionality
from keyboards.inline.referral_stuff import referral_system
from loader import dp, db, bot


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_referral_system"))
async def show_referral_system(call: types.CallbackQuery):
    user = await db.select_user(call.from_user.id)
    referrer_id = user['referrer_id']
    if referrer_id == -1001594274069:
        message_text = "Вы пришли из канала @desk_setup_channel"
    else:
        referrer = await bot.get_chat_member(referrer_id, referrer_id)
        referrer_username = referrer['user']['username']
        message_text = f"Вас пригласил пользователь @{referrer_username}"
    await call.message.answer(message_text, reply_markup=referral_system)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="create_referral_link"))
async def create_referral_link(call: types.CallbackQuery):
    deep_link = await get_start_link(payload=call.from_user.id)
    await call.message.answer(f"Ваша пригласительная ссылка:\n"
                              f"<u>{deep_link}</u>")
