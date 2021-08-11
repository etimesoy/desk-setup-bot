from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from keyboards.inline.callback_data import bot_functionality
from keyboards.inline.referral_stuff import referral_system
from loader import dp


@dp.callback_query_handler(bot_functionality.filter(functionality_name="show_referral_system"))
async def show_referral_system(call: types.CallbackQuery):
    await call.message.answer("Вас пригласил пользователь/группа ........",
                              reply_markup=referral_system)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="create_referral_link"))
async def create_referral_link(call: types.CallbackQuery):
    deep_link = await get_start_link(payload=call.from_user.id)
    await call.message.answer(f"Ваша пригласительная ссылка:\n"
                              f"<u>{deep_link}</u>")
