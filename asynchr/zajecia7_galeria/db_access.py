import asyncio
import datetime
import io
from dataclasses import dataclass
from typing import List, Tuple

import aiosqlite
from PIL import Image, ImageOps
from PIL.Image import BICUBIC
from aiosqlite.core import Connection

from asynchr.zajecia7_galeria.helpers import row_2_picture, file_2_picture
from asynchr.zajecia7_galeria.model import Picture, User
from utils.profile import ts

"""
Prosty dostęp do bazy (linux): 
apt install sqlite
sqlite3 pic_db.db
--> konsola z dostępem do danych


Re connections: 
https://stackoverflow.com/questions/53908615/reusing-aiosqlite-connection/70410761#70410761

- zapisy blokują całą bazę danych, więc nie ma sensu używać jednego connection dla wszystkich zapisów
- pojedyncze otwarcie "connection" to 0.4ms
- można używać wspólnego connection dla read-only queries

"""


class DbService:
    db: Connection  # connection for read-only access
    filename: str

    def __init__(self, filename):
        self.filename = filename

    async def create_tables(self):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('create table if not exists pictures (pictureid INTEGER PRIMARY KEY AUTOINCREMENT, '
                             'data BLOB, data_thumbnail TEXT, filename TEXT, description TEXT, creator_userid INT, '
                             'created REAL)')
            # await db.execute('create table if not exists users (userid INTEGER PRIMARY KEY AUTOINCREMENT, '
            #                  'name TEXT, pass_sha256 TEXT, token TEXT, active BOOL)')
            await db.commit()

    async def insert_picture(self, pic: Picture):
        now: float = datetime.datetime.now().timestamp()
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute(
                    'INSERT INTO pictures (data, data_thumbnail, filename, description, creator_userid, created) '
                    'values(?,?,?,?,?,?)',
                    (pic.data, pic.data_thumbnail, pic.filename, pic.description, pic.creator_userid, now)) as cursor:
                pic.pictureid = cursor.lastrowid
                await db.commit()
        return pic

    async def delete_pictures(self):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('delete from pictures where true')
            await db.commit()

    async def insert_user(self, user: User) -> User:
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute('INSERT INTO users (name, pass_sha256, token, active) '
                                  'values(?,?,?,?)', (user.name, user.pass_sha256, '', True)) as cursor:
                user.userid = cursor.lastrowid
                await db.commit()
        return user

    async def test_connect_speed(self):
        # ~ 2000 connections per second
        st = ts()
        x = 0
        for i in range(1000):
            async with aiosqlite.connect(self.filename) as db:
                async with db.execute('SELECT 12', ()) as cursor:
                    x += 1
        en = ts()
        print(f'execution took {en - st:.3f}s')

    async def update_pic(self, db, pictureid: int, name: str):
        # todo
        await db.execute('UPDATE pic SET name=? WHERE id=?', (name, pictureid,))
        await db.commit()

    # READ ONLY ACCESS

    async def fetch_thumbnails_all_pictures(self, limit=100) -> List[Picture]:
        # uwaga: w systemie galerii powinien zwrócić obrazki _bez_ głównego pola "data"
        ans = []
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute('SELECT pictureid, data_thumbnail, filename, description, creator_userid, created'
                                  ' FROM pictures LIMIT ?', (limit,)) as cursor:
                async for row in cursor:
                    ans.append(row_2_picture(row, with_data=False))
        return ans

    async def fetch_picture(self, pictureid) -> Picture:
        # pojedynczy obrazek, ale z wszystkimi danymi
        ans = []
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute('SELECT * FROM pictures where pictureid=?', (pictureid,)) as cursor:
                async for row in cursor:
                    ans.append(row_2_picture(row, with_data=True))
        return ans[0]

    async def fetch_user(self, userid) -> User:
        # pojedynczy user
        ans = []
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute('SELECT * FROM users where userid=?', (userid,)) as cursor:
                async for row in cursor:
                    ans.append(User(*row))
        return ans[0]

    async def fetch_users(self) -> List[User]:
        ans = []
        async with aiosqlite.connect(self.filename) as db:
            async with db.execute('SELECT * FROM users', ()) as cursor:
                async for row in cursor:
                    ans.append(User(*row))
        return ans


async def db1():
    db = DbService('pic_db.db')
    # await db.create_tables()
    # user = await db.insert_user(User(-1, 'Leonardi', 'xxx', '', True))
    # print(user)
    # print(await fetch_users(db))
    # print(await fetch_thumbnails_all_pictures(db, 10))

    pic: Picture = file_2_picture('sample.png')
    p = await db.insert_picture(pic)
    print(p.pictureid, p.filename, p.created, p.data_thumbnail)

    # p = await db.fetch_picture(11)

    # for pic in await fetch_thumbnails_all_pictures(db):
    #     await pil_image_from_picture(pic)

    # pic = (await fetch_picture(db, 6))
    # await pil_image_from_picture(pic)

    # await insert_pic(db, 'ggx')
    # await update_pic(db, 1, '_gg')
    # await delete_pic(db, pictureid=2)
    # print(await fetch_thumbnails_all_pic(db))
    # print(await fetch_pic(db, 1))


if __name__ == '__main__':
    asyncio.run(db1())
