from typing import Union

from asyncpg import UniqueViolationError
import asyncpg
from asyncpg import Pool, Connection
from tgbot.data.config import load_config

config = load_config(".env")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS usersmanage_user (
        user_id BIGINT PRIMARY KEY
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_item(self):
        sql = """
        CREATE TABLE IF NOT EXISTS usersmanage_item (
        item_id SERIAL PRIMARY KEY,
        category VARCHAR(50) NOT NULL,
        subcategory VARCHAR(50) NOT NULL,
        photo_id VARCHAR(100) NOT NULL,
        description VARCHAR(100) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_order(self):
        sql = """
        CREATE TABLE IF NOT EXISTS usersmanage_order (
        order_id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        item_id INT NOT NULL,
        count INT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql: str, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    # async def select_items(self, **kwargs):
    #     sql = "SELECT * FROM usersmanage_item WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetch=True)

    async def add_user(self, user_id: int):
        try:
            sql = """
            INSERT INTO usersmanage_user (user_id)
            VALUES ($1)
            """
            return await self.execute(sql, user_id, execute=True)
        except UniqueViolationError:
            pass

    async def select_all_users(self):
        sql = "SELECT * FROM usersmanage_user"
        res = await self.execute(sql, fetch=True)
        return [x.get("user_id") for x in res]

    async def add_item(
        self, category: str, subcategory: str, photo_id: str, description: str
    ):
        sql = """
        INSERT INTO usersmanage_item (category, subcategory, photo_id, description)
        VALUES ($1, $2, $3, $4)
        """
        return await self.execute(
            sql, category, subcategory, photo_id, description, execute=True
        )

    async def select_categories(self):
        sql = """
        SELECT category 
        FROM usersmanage_item 
        GROUP BY category 
        ORDER BY category
        """
        res = await self.execute(sql, fetch=True)
        return [x.get("category") for x in res]

    async def select_subcategories(self, category: str):
        sql = """
        SELECT subcategory 
        FROM usersmanage_item 
        WHERE category = $1
        GROUP BY subcategory 
        ORDER BY subcategory
        """
        res = await self.execute(sql, category, fetch=True)
        return [x.get("subcategory") for x in res]

    async def select_items(self, category: str, subcategory: str):
        sql = """
        SELECT * 
        FROM usersmanage_item 
        WHERE category = $1 AND subcategory = $2
        ORDER BY item_id
        """
        res = await self.execute(sql, category, subcategory, fetch=True)
        return res

    async def select_one_item(self, item_id: int):
        sql = """
        SELECT * 
        FROM usersmanage_item 
        WHERE item_id = $1 
        """
        res = await self.execute(sql, item_id, fetchrow=True)
        return res

    async def add_order(self, user_id: int, item_id: int, count: int):
        sql = """
        INSERT INTO usersmanage_order (user_id, item_id, count)
        VALUES ($1, $2, $3)
        """
        return await self.execute(sql, user_id, item_id, count, execute=True)

    async def delete_order(self, order_id):
        sql = """
        DELETE FROM usersmanage_order WHERE order_id = $1
        """
        return await self.execute(sql, order_id, execute=True)

    async def select_user_orders(self, user_id):
        sql = """
        SELECT * FROM usersmanage_order WHERE user_id = $1
        """
        res = await self.execute(sql, user_id, fetch=True)
        return res

    async def select_order(self, order_id: int):
        sql = """
        SELECT * 
        FROM usersmanage_order 
        WHERE order_id = $1 
        """
        res = await self.execute(sql, order_id, fetchrow=True)
        return res


async def on_startup(db: Database):
    await db.create()
