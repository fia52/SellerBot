import asyncio

from tgbot.data.content import categories_dict
from tgbot.models.db_funcs_sql import Database


async def test():
    db = Database()
    await db.create()

    await db.create_table_user()
    await db.create_table_item()
    await db.create_table_order()

    # print("Добавляем пользователей")
    # await db.add_user(user_id=1003082911)
    # await db.add_user(user_id=2003082911)
    # await db.add_user(user_id=3003082911)
    # await db.add_user(user_id=4003082911)
    # print("Готово")
    #
    # users = await db.select_all_users()
    # print(f"all users: {users}")
    # # print(f"first user id: {users[0].user_id}")

    print("Добавляем items")
    for category in categories_dict:
        for subcategory in categories_dict.get(category):
            for item in categories_dict.get(category).get(subcategory):
                await db.add_item(
                    category=category,
                    subcategory=subcategory,
                    photo_id="AgACAgIAAxkBAAN8ZDKeShLsoCB1FKqFl_-nqQ13KV8AAq7HMRvmz5FJhPSiRV1PT3YBAAMCAANzAAMvBA",
                    description=item,
                )

    print("all items added")

    # categories = await db.select_categories()
    # print(f"categories:  {categories}")
    #
    # subcategories = await db.select_subcategories(category="Категория 1")
    # print(f"subcategories:  {subcategories}")
    #
    # items = await db.select_items(category="Категория 1", subcategory="Подкатегория 2")
    # print(f"items: {items}")
    #
    # await db.add_order(user_id=1003082911, item_id=3, count=2)
    # await db.add_order(user_id=1003082911, item_id=4, count=1)
    # await db.add_order(user_id=1003082911, item_id=5, count=6)
    #
    # orders = await db.select_user_orders(user_id=1003082911)
    # print(f"orders of 1003082911: {orders}")
    #
    # print("deletion")
    # await db.delete_order(order_id=1)
    # await db.delete_order(order_id=2)
    #
    # orders = await db.select_user_orders(user_id=1003082911)
    # print(f"orders of 1003082911 aft del: {orders}")
    # print(orders[0].get("user_id"))
    #
    # item = await db.select_one_item(item_id=201)
    # print(item)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
