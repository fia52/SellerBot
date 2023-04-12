from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.data.config import Config
from tgbot.keyboards.inline import required_chats
from loader import bot


class IsSubscriber(BoundFilter):
    async def check(self, obj: types.Message) -> bool:
        config: Config = obj.bot.get("config")
        for chat_id in config.tg_bot.required_chat_ids:
            sub = await bot.get_chat_member(chat_id=chat_id, user_id=obj.from_user.id)
            if sub.status == types.ChatMemberStatus.LEFT:
                await obj.reply(
                    text="Подпишитесь на группу и канал, после повторите попытку",
                    reply_markup=required_chats,
                )
                return False

        return True
