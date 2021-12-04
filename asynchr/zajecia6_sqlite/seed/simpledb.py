import asyncio
from dataclasses import dataclass
from typing import List

import aiosqlite
from aiosqlite.core import Connection


@dataclass
class User:
    name: str
    pesel: str
    age: int


async def create_table_users(db: Connection):
    await db.execute("create table users (name text, pesel text, age int)")
    await db.commit()


async def insert_user(db):
    await db.execute('INSERT INTO users(name, pesel, age) values("xi", "123", ?)', (38,))
    await db.commit()


async def purge_users(db):
    await db.execute('DELETE FROM users where age>?', (80,))
    await db.commit()


async def fetch_users(db) -> List[dict]:
    ans = []
    async with db.execute("SELECT * FROM users") as cursor:
        async for row in cursor:
            print(User(*row))
    return ans


async def fetch_one_user(db: Connection) -> User:
    async with db.execute('SELECT * FROM users where name="xi"') as cursor:
        u = await cursor.fetchone()
        if u:
            print(u)
            print(User(*u))
            return User(*u)
        else:
            return None



async def db1():
    async with aiosqlite.connect('a.db') as db:
        # await create_table_users(db)
        await insert_user(db)
        await fetch_one_user(db)
        await fetch_users(db)
        # await purge_users(db)


async def other():
    await db1()
    print('finished')


asyncio.run(other())
