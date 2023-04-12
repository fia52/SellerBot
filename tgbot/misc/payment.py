from aiogram.types import LabeledPrice, CallbackQuery

from tgbot.data.config import load_config


async def payment(callback: CallbackQuery, data):
    config = load_config(".env")
    await callback.message.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=data.get("description"),
        description=data.get("description"),
        payload=f"{data.get('item_id')}",
        provider_token=config.misc.yookassa_token,
        currency="RUB",
        start_parameter="test_bot",
        prices=[{"label": "Руб", "amount": 40000}],
        need_shipping_address=True,
    )
