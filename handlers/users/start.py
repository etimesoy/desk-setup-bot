import re
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import get_bot_functionality
from keyboards.inline.referral_stuff import referral_buttons
from keyboards.inline.callback_data import bot_functionality
from loader import dp, db


@dp.message_handler(CommandStart(deep_link=re.compile(r"^\d{4,15}$")))
@dp.message_handler(CommandStart(deep_link="-1001594274069"))
async def bot_start_with_deep_link(message_or_call: Union[types.Message, types.CallbackQuery],
                                   referrer_id: int = None):
    if isinstance(message_or_call, types.Message):
        message = message_or_call
    else:
        message = message_or_call.message
    if referrer_id is None:
        referrer_id = int(message.get_args())
    user_full_name = message_or_call.from_user.full_name
    user_id = message_or_call.from_user.id
    username = message_or_call.from_user.username
    if await db.select_user(user_id) is None:
        await db.add_user(user_id, referrer_id, user_full_name, username)
    await message.answer(f"Привет, {user_full_name}! "
                         f"Добро пожаловать в магазин клевых вещей для твоего рабочего места😉\n"
                         f"Вот, что я умею:", reply_markup=get_bot_functionality(user_id))


@dp.message_handler(CommandStart())
async def bot_start_without_deep_link(message: types.Message,
                                      user_id: int = None, user_full_name: str = None):
    if user_full_name is None:
        user_full_name = message.from_user.full_name
    if user_id is None:
        user_id = message.from_user.id
    user = await db.select_user(user_id)
    if user is None:
        await message.answer(f"Привет, {user_full_name}! "
                             f"Чтобы пользоваться ботом, нужно зарегистрироваться в реферальной программе.\n"
                             f"Выбери способ:", reply_markup=referral_buttons)
    else:
        await bot_start_with_deep_link(message, user['referrer_id'])


@dp.callback_query_handler(bot_functionality.filter(functionality_name="check_channel_subscription"))
async def check_channel_subscription(call: types.CallbackQuery):
    # if call.message.chat.id in await get_channel_participants(-1001594274069):
    #     await bot_start_with_deep_link(call.message, referrer_id=-1001594274069)
    # TODO: проверить подписку пользователя на канал
    await bot_start_with_deep_link(call, referrer_id=-1001594274069)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="back"), state="enter_referrer_id")
async def back_to_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.reset_state()
    user_full_name = call.from_user.full_name
    user_id = call.from_user.id
    await bot_start_without_deep_link(call.message, user_id, user_full_name)


@dp.callback_query_handler(bot_functionality.filter(functionality_name="enter_referrer_id"))
async def enter_referrer_id(call: types.CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton("Назад", callback_data=bot_functionality.new("back"))
    ]])
    await call.message.edit_text("Введите ID пользователя, который пригласил вас",
                                 reply_markup=back_button)
    await state.set_state("enter_referrer_id")


@dp.message_handler(state="enter_referrer_id")
async def save_referrer_id(message: types.Message, state: FSMContext):
    await state.reset_state()
    # TODO: добавить проверку правильности ввода id реферрера
    await bot_start_with_deep_link(message, referrer_id=int(message.text))
