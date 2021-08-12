from typing import Optional, List

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            # port=config.DB_HOST,
            # host='db',
            database=config.DB_NAME
        )

    async def _execute(self, command: str, *args, fetch_all=False, fetch_row=False,
                       fetch_val=False, execute=False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch_all:
                    result = await connection.fetch(command, *args)
                elif fetch_row:
                    result = await connection.fetchrow(command, *args)
                elif fetch_val:
                    result = await connection.fetchval(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def _create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            referrer_id BIGINT NOT NULL REFERENCES Users(telegram_id),
            full_name VARCHAR(255) NOT NULL,
            username VARCHAR(255),
            email VARCHAR(255)
        );
        """
        await self._execute(sql, execute=True)

    async def _create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            photo_link TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT
        );
        """
        await self._execute(sql, execute=True)

    async def _create_table_baskets(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Baskets (
            id SERIAL PRIMARY KEY,
            user_telegram_id BIGINT NOT NULL REFERENCES USERS(telegram_id),
            product_id BIGINT NOT NULL REFERENCES PRODUCTS(id),
            product_quantity INTEGER NOT NULL
        );
        """
        await self._execute(sql, execute=True)

    async def create_standard_tables(self):
        await self._create_table_users()
        await self._create_table_products()
        await self._create_table_baskets()

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${idx + 1}" for idx, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    # section: Working with table Users

    async def add_user(self, telegram_id: int, referrer_id: int,
                       full_name: str, username: str):
        sql = "INSERT INTO Users (telegram_id, referrer_id, full_name, username) " \
              "VALUES ($1, $2, $3, $4) returning *"
        return await self._execute(sql, telegram_id, referrer_id, full_name, username, fetch_row=True)

    async def update_email_for_user(self, telegram_id: int, email: str):
        sql = "UPDATE Users SET email = $1 WHERE telegram_id = $2"
        await self._execute(sql, email, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self._execute(sql, fetch_all=True)

    async def select_user(self, telegram_id: int):
        sql = "SELECT * FROM Users WHERE telegram_id = $1"
        return await self._execute(sql, telegram_id, fetch_row=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self._execute(sql, fetch_val=True)

    async def update_user_username(self, username: str, telegram_id: int):
        sql = "UPDATE Users SET username = $1 WHERE telegram_id = $2"
        return await self._execute(sql, username, telegram_id, execute=True)

    # section: Working with table Products

    async def select_all_products(self):
        sql = "SELECT * FROM Products"
        return await self._execute(sql, fetch_all=True)

    async def add_product(self, name: str, photo_link: str, price: int, description: str):
        sql = "INSERT INTO Products (name, photo_link, price, description) VALUES ($1, $2, $3, $4)"
        await self._execute(sql, name, photo_link, price, description, execute=True)

    # async def delete_product(self, name: str, photo_link: str, price: int, description: str):
    #     sql = "DELETE FROM Products WHERE name = $1 AND photo_link = $2 AND price = $3 AND description = $4"
    #     await self._execute(sql, name, photo_link, price, description, execute=True)
    async def delete_product(self, product_id: int):
        sql = "DELETE FROM Products WHERE id = $1"
        await self._execute(sql, product_id, execute=True)

    async def delete_all_products(self):
        sql = "DELETE FROM Products WHERE TRUE"
        await self._execute(sql, execute=True)

    async def update_product_description(self, product_id: int, new_description: str):
        sql = "UPDATE Products SET description = $1 WHERE id = $2"
        await self._execute(sql, new_description, product_id, execute=True)

    # section: Working with table Baskets

    async def select_all_products_for_user(self, user_telegram_id: int):
        sql = "SELECT product_id, product_quantity, name, photo_link, price, description " \
              "FROM Baskets JOIN Products ON Baskets.product_id = Products.id " \
              "WHERE user_telegram_id = $1"
        return await self._execute(sql, user_telegram_id, fetch_all=True)

    async def add_product_for_user(self, user_telegram_id: int,
                                   product_id: int, product_quantity: int):
        sql = "INSERT INTO Baskets (user_telegram_id, product_id, product_quantity) VALUES ($1, $2, $3)"
        await self._execute(sql, user_telegram_id, product_id, product_quantity, execute=True)

    async def change_product_quantity_for_user(self, user_telegram_id: int,
                                               product_id: int, product_quantity: int):
        sql = "UPDATE Baskets SET product_quantity = $1 WHERE " \
              "user_telegram_id = $2 AND product_id = $3"
        return await self._execute(sql, user_telegram_id, product_id, product_quantity, execute=True)

    async def delete_product_for_user(self, user_telegram_id: int, product_id: int):
        sql = "DELETE FROM Baskets WHERE user_telegram_id = $1 AND product_id = $2"
        return await self._execute(sql, user_telegram_id, product_id, execute=True)
