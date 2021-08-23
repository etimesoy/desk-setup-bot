import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink, hcode

from data import config
from handlers.inline_mode import get_inline_results_for_query
from keyboards.inline import paid_keyboard
from keyboards.inline.callback_data import inline_mode_product
from loader import dp, db
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


async def check_user(query: types.InlineQuery) -> bool:
    telegram_id = query.from_user.id
    user = await db.select_user(telegram_id)
    if user is None:
        await query.answer(
            results=[],
            switch_pm_text="Бот недоступен. Подключить бота",
            switch_pm_parameter="from_inline_mode"
        )
    return bool(user)


@dp.inline_handler(regexp=re.compile(r".."))
@dp.inline_handler(text="")
async def some_query(query: types.InlineQuery):
    if not await check_user(query):
        return

    await query.answer(results=await get_inline_results_for_query(query.chat_type, query.query), cache_time=1)


@dp.callback_query_handler(inline_mode_product.filter(action="show"))
async def show_product(call: types.CallbackQuery, callback_data: dict,
                       state: FSMContext, message: types.Message = None):
    product_id = int(callback_data["id"])
    product = await db.get_product_info(product_id)
    await state.update_data(product_id=product_id)
    await state.update_data(product_name=product["name"])
    await state.update_data(product_price=product["price"])
    message_text = product["name"] + " - " + str(product["price"]) + "₽\n" + \
                   product["description"] + '\n' + \
                   f"<a href='{product['photo_link']}'>thumbnail</a>"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton("Купить", callback_data=inline_mode_product.new(
            callback_data["id"], "buy"
        ))
    ]])
    if message:
        await message.answer(message_text, reply_markup=markup)
    else:
        await call.bot.send_message(call.from_user.id, message_text,
                                    reply_markup=markup)


@dp.callback_query_handler(inline_mode_product.filter(action="buy"))
async def buy_product(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите количество товара")
    await state.set_state("enter_quantity")


@dp.message_handler(state="enter_quantity")
async def enter_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, введите заново")
        return
    await state.update_data(product_quantity=quantity)
    await message.answer("Введите адрес доставки")
    await state.set_state("enter_address")


@dp.message_handler(state="enter_address")
async def create_invoice(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    product = await state.get_data()
    amount = int(product['product_quantity']) * int(product['product_price'])

    payment = Payment(amount=amount)
    payment.create()

    await message.answer('\n'.join([
        f"Товар: {product['product_name']}",
        f"Количество: {product['product_quantity']}",
        f"Общая стоимость: {amount}",
        f"Адрес: {product['address']}",
        f"Оплатите не менее {amount:.2f}₽ по номеру телефона или по адресу",
        "",
        hlink(config.WALLET_QIWI, url=payment.invoice),
        "И обязательно укажите ID платежа:",
        hcode(payment.id)
    ]), reply_markup=paid_keyboard)

    await state.set_state("qiwi")
    await state.update_data(payment=payment)


@dp.callback_query_handler(text="cancel", state="qiwi")
async def cancel_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отменено")
    await state.finish()


@dp.callback_query_handler(text="paid", state="qiwi")
async def approve_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")

    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена.")
        return
    except NotEnoughMoney:
        await call.message.answer("Оплаченная сума меньше необходимой.")
        return
    else:
        await call.message.answer("Успешно оплачено")

    await call.message.edit_reply_markup()
    await state.finish()
