import asyncio
from dataclasses import dataclass
from typing import List

import aiosqlite
from aiosqlite.core import Connection


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


async def update_pic(db, pictureid: int, name: str):
    await db.execute('UPDATE pic SET name=? WHERE id=?', (name, pictureid,))
    await db.commit()


async def delete_pic(db, pictureid):
    await db.execute('DELETE FROM pic WHERE id=?', (pictureid,))
    await db.commit()


async def fetch_all_pic(db):
    ans = []
    async with db.execute('SELECT * FROM pic') as cursor:
        async for row in cursor:
            ans.append(Pic(*row))
    return ans


async def db1():
    async with aiosqlite.connect('pic_db.db') as db:
        # await create_table_pic(db)
        # await insert_pic(db, 'ggx')
        # await update_pic(db, 1, '_gg')
        # await delete_pic(db, pictureid=2)
        print(await fetch_all_pic(db))


asyncio.run(db1())
