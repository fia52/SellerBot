from loader import db, bot


async def sendall(text):
    await db.create()
    ids = await db.select_all_users()
    for tg_id in ids:
        try:
            await bot.send_message(chat_id=tg_id, text=text)
        except Exception:
            pass
