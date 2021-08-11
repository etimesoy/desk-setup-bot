from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline import get_bot_functionality
from loader import dp


@dp.message_handler(Command("menu"))
@dp.message_handler(Text(equals="Главное меню"), state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.delete()
    await message.answer("<b>Главное меню</b>",
                         reply_markup=get_bot_functionality(message.from_user.id))
