import re
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline import get_bot_functionality
from keyboards.inline.referral_stuff import referral_buttons
from keyboards.inline.callback_data import bot_functionality
from loader import dp
from utils.misc import get_channel_participants


@dp.message_handler(CommandStart(deep_link=re.compile(r"^\d{4,15}$")))
@dp.message_handler(CommandStart(deep_link="desk_setup_channel"))
async def bot_start_with_deep_link(message_or_call: Union[types.Message, types.CallbackQuery]):
    if isinstance(message_or_call, types.Message):
        message = message_or_call
    else:
        message = message_or_call.message
    user_full_name = message_or_call.from_user.full_name
    user_id = message_or_call.from_user.id
    await message.answer(f"Привет, {user_full_name}! "
                         f"Добро пожаловать в магазин клевых вещей для твоего рабочего места😉\n"
                         f"Вот, что я умею:", reply_markup=get_bot_functionality(user_id))


@dp.message_handler(CommandStart())
async def bot_start_without_deep_link(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Чтобы пользоваться ботом, нужно зарегистрироваться в реферальной программе.\n"
                         f"Выбери способ:", reply_markup=referral_buttons)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="check_channel_subscription"))
async def check_channel_subscription(call: types.CallbackQuery):
    # if call.message.chat.id in await get_channel_participants(-1001594274069):
    #     await bot_start_with_deep_link(call.message)
    # TODO: проверить подписку пользователя на канал
    # TODO: сохранить id канала как реферера пользователя
    await bot_start_with_deep_link(call)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="enter_referrer_id"))
async def enter_referrer_id(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID пользователя, который пригласил вас")
    await state.set_state("enter_referrer_id")


@dp.message_handler(state="enter_referrer_id")
async def save_referrer_id(message: types.Message, state: FSMContext):
    # TODO: сохранить ID пригласившего в базу данных
    await state.reset_state()
    await bot_start_with_deep_link(message)
