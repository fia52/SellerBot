from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.filters.subscriber_check import IsSubscriber
from tgbot.keyboards.inline import main_menu
from tgbot.keyboards.callback_datas import pagination_call
from loader import db


async def user_start(message: Message):
    await db.add_user(message.from_user.id)
    await message.reply("Привет! Чем могу помочь?", reply_markup=main_menu)


async def current_page_button_pressed(callback: CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=60)


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start, IsSubscriber(), commands=["start", "menu"], state="*"
    )
    dp.register_callback_query_handler(
        current_page_button_pressed, pagination_call.filter(page="empty"), state="*"
    )
