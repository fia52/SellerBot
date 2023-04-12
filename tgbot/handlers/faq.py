from aiogram import Dispatcher
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.markdown import hbold

from tgbot.data.content import questions_and_answers
from loader import dp


@dp.inline_handler(text="FAQ")
async def show_question(query: InlineQuery):
    photo_url = "https://cdn-icons-png.flaticon.com/512/237/237879.png"
    Q_A = await questions_and_answers(query.query)
    result = []
    for number, item in enumerate(Q_A, start=1):
        result.append(
            InlineQueryResultArticle(
                id=number,
                title=item,
                input_message_content=InputTextMessageContent(
                    message_text=f"{hbold(item)}\n\n" + Q_A[item],
                    disable_web_page_preview=True,
                ),
                thumb_url=photo_url,
                description=Q_A[item][:20] + "...",
            )
        )

    await query.answer(results=result)
