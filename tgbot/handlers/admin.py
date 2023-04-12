from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.filters.subscriber_check import IsSubscriber


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def get_photo(message: Message):
    await message.reply(f"photo_id: {message.photo[0].file_id}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, IsSubscriber(), commands=["start"], state="*", is_admin=True
    )

    dp.register_message_handler(get_photo, content_types=["photo"])
