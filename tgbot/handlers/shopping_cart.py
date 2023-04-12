from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import db, wb
from tgbot.keyboards.inline import (
    get_shopping_cart_keyboard,
    confirm_keyboard,
    main_menu,
)
from tgbot.keyboards.callback_datas import make_order_call, delete_order_call
from tgbot.misc.payment import payment


async def show_shopping_cart(callback: CallbackQuery):
    await callback.answer()

    orders = await db.select_user_orders(user_id=callback.from_user.id)

    await callback.message.answer("Ваша корзина:")
    for order in orders:
        item = await db.select_one_item(item_id=order.get("item_id"))
        description = item.get("description")
        count = order.get("count")
        order_id = order.get("order_id")
        await callback.message.answer(
            text=f"{description}: {count} шт.",
            reply_markup=get_shopping_cart_keyboard(order_id=order_id),
        )


async def delete_order(callback: CallbackQuery, callback_data: dict):
    await callback.answer()

    await db.delete_order(order_id=int(callback_data.get("order_id")))

    await callback.message.answer("Удалено")
    await callback.message.bot.delete_message(
        chat_id=callback.from_user.id, message_id=callback.message.message_id
    )


class MakeOrderFSM(StatesGroup):
    waiting_for_address = State()
    waiting_for_confirm = State()
    waiting_for_payment = State()


async def making_order_start(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    await callback.answer()

    await MakeOrderFSM.waiting_for_address.set()

    order = await db.select_order(order_id=int(callback_data.get("order_id")))

    item = await db.select_one_item(item_id=order.get("item_id"))
    description = item.get("description")

    async with state.proxy() as data:
        data["order_id"] = order.get("order_id")
        data["description"] = description
        data["item_id"] = order.get("item_id")
        data["user_id"] = order.get("user_id")
        data["count"] = order.get("count")

    await callback.message.answer("В своём следующем сообщении укажите адрес доставки:")


async def obtain_address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text

    description = data.get("description")
    count = data.get("count")
    address = data.get("address")

    await message.answer(
        text=f"Подтвердите информацию о заказе:\n товар: {description} \n кол-во: {count}"
        f" \n адрес доставки: {address} \n Перейдём к оплате?",
        reply_markup=confirm_keyboard,
    )

    await MakeOrderFSM.next()


async def obtain_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if callback.data == "Да":
        async with state.proxy() as data:
            await wb.put_in_excel(data)  #
            await callback.message.answer("Заказ создан!", reply_markup=main_menu)  #
            await state.finish()  #
            # await payment(callback, data)
            # await MakeOrderFSM.next()
    else:
        await callback.message.answer(text="хорошо (")
        await show_shopping_cart(callback)
        await state.finish()


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True
    )


async def obtain_payment(message: Message, state: FSMContext):
    async with state.proxy() as data:
        # if message.successful_payment.invoice_payload == data.get("item_id"):
        await wb.put_in_excel(data)
        await message.answer("Заказ создан!", reply_markup=main_menu)

        await state.finish()


def register_shopping_cart(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_shopping_cart, lambda x: x.data and x.data == "shopping_cart", state="*"
    ),
    dp.register_callback_query_handler(delete_order, delete_order_call.filter()),
    dp.register_callback_query_handler(
        making_order_start, make_order_call.filter(), state="*"
    ),
    dp.register_message_handler(
        obtain_address, content_types=["text"], state=MakeOrderFSM.waiting_for_address
    ),
    dp.register_callback_query_handler(
        obtain_confirm,
        lambda x: x.data and x.data in ["Да", "Нет"],
        state=MakeOrderFSM.waiting_for_confirm,
    )
    dp.pre_checkout_query_handler(
        process_pre_checkout_query, state=MakeOrderFSM.waiting_for_payment
    ),
    dp.message_handler(
        obtain_payment,
        content_types=ContentType.SUCCESSFUL_PAYMENT,
        state=MakeOrderFSM.waiting_for_payment,
    )
