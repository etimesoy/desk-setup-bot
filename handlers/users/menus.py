from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline import get_bot_functionality
from keyboards.inline.callback_data import bot_functionality
from loader import dp, db


@dp.message_handler(Command("menu"))
@dp.message_handler(Text(equals="Главное меню"), state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    if await db.select_user(message.from_user.id):
        await state.reset_state()
        await message.delete()
        await message.answer("<b>Главное меню</b>",
                             reply_markup=get_bot_functionality(message.from_user.id))
    else:
        await message.answer("Чтобы пользоваться ботом, нужно зарегистрироваться в реферальной программе")


@dp.callback_query_handler(bot_functionality.filter(functionality_name="answer_menu"))
async def answer_main_menu(call: types.CallbackQuery):
    await call.message.answer("<b>Главное меню</b>",
                              reply_markup=get_bot_functionality(call.from_user.id))
