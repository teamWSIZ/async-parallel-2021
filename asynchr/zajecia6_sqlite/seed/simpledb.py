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
    await db.execute('create table users (name text, pesel text, age int)')
    await db.commit()
    print('table created')


async def insert_user(db, age=38):
    await db.execute('INSERT INTO users(name, pesel, age) values("xi", "123", ?)', (age,))
    await db.commit()


async def purge_users(db, max_age=80):
    await db.execute('DELETE FROM users where age>?', (max_age,))
    await db.commit()


# z = (1,2,3)
# *z --> 1,2,3

async def fetch_users(db) -> List[User]:
    ans = []
    async with db.execute('SELECT * FROM users') as cursor:
        async for row in cursor:
            # print(row)
            # print(User(*row))
            ans.append(User(*row))
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


@dataclass
class Pic:
    id: int
    name: str


async def create_table_pic(db: Connection):
    await db.execute('create table pic (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)')
    await db.commit()
    print('table created')


async def insert_pic(db, name):
    await db.execute('INSERT INTO pic(name) values(?)', (name,))
    await db.commit()


async def fetch_all_pic(db):
    ans = []
    async with db.execute('SELECT * FROM pic') as cursor:
        async for row in cursor:
            # print(row)
            # print(User(*row))
            ans.append(Pic(*row))
    return ans


async def db1():
    async with aiosqlite.connect('a.db') as db:
        # await create_table_pic(db)
        await insert_pic(db, 'gg')
        print(await fetch_all_pic(db))

        # await create_table_users(db)
        # await insert_user(db, 21)
        # await fetch_one_user(db)
        # print(await fetch_users(db))
        # await purge_users(db, 30)
        # print(await fetch_users(db))

if __name__ == '__main__':
    asyncio.run(db1())
