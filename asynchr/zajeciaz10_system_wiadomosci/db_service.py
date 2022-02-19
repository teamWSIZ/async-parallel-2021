import asyncio
from dataclasses import dataclass
from typing import List

import aiosqlite
from aiosqlite.core import Connection


async def create_table_users(db: Connection):
    await db.execute('create table users (name text, password text)')
    await db.commit()
    print('table created')


async def insert_user(db, username, password):
    async with db.execute('select * from users where name=?', (username,)) as cursor:
        async for row in cursor:
            raise RuntimeError(f'user {username} already exists')

    await db.execute('INSERT INTO users(name, password) values(?,?)', (username, password))
    await db.commit()
    # print('done')


@dataclass
class User:
    name: str
    password: str


async def fetch_users(db) -> List[User]:
    ans = []
    async with db.execute('SELECT * FROM users') as cursor:
        async for row in cursor:
            ans.append(User(*row))
    return ans


async def db1():
    async with aiosqlite.connect('users_topics.db') as db:
        # await create_table_users(db)
        await insert_user(db, 'abra', 'kadabra')
        print(await fetch_users(db))

        # await create_table_users(db)
        # await insert_user(db, 21)
        # await fetch_one_user(db)
        # print(await fetch_users(db))
        # await purge_users(db, 30)
        # print(await fetch_users(db))


if __name__ == '__main__':
    asyncio.run(db1())
