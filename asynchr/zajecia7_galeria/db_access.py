import asyncio
import datetime
import io
from dataclasses import dataclass
from typing import List, Tuple

import aiosqlite
from PIL import Image, ImageOps
from PIL.Image import BICUBIC
from aiosqlite.core import Connection

from asynchr.zajecia7_galeria.model import Picture, User


@dataclass
class Pic:
    id: int
    name: str
    created: float


async def create_table_pic(db: Connection):
    await db.execute('create table pic (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, created REAL)')
    await db.commit()
    print('table created')


async def create_tables(db: Connection):
    # await db.execute('drop table pictures')
    await db.execute('create table if not exists pictures (pictureid INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'data BLOB, data_thumbnail BLOB, filename TEXT, description TEXT, creator_userid INT, '
                     'created REAL)')
    await db.execute('create table if not exists users (userid INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'name TEXT, pass_sha256 TEXT, token TEXT, active BOOL)')
    await db.commit()
    print('tables created')


async def insert_picture(db, pic: Picture):
    now: float = datetime.datetime.now().timestamp()
    await db.execute('INSERT INTO pictures (data, data_thumbnail, filename, description, creator_userid, created) '
                     'values(?,?,?,?,?,?)',
                     (pic.data, pic.data_thumbnail, pic.filename, pic.description, pic.creator_userid, now))
    await db.commit()


async def delete_pictures(db):
    await db.execute('delete from pictures where true')
    await db.commit()


async def delete_users(db):
    await db.execute('delete from users where true')
    await db.commit()


async def insert_user(db, user: User) -> User:
    async with db.execute('INSERT INTO users (name, pass_sha256, token, active) '
                          'values(?,?,?,?)', (user.name, user.pass_sha256, '', True)) as cursor:
        print(cursor.lastrowid)
        user.userid = cursor.lastrowid
    return user


async def update_pic(db, pictureid: int, name: str):
    await db.execute('UPDATE pic SET name=? WHERE id=?', (name, pictureid,))
    await db.commit()


async def get_thumbnail(image: Image) -> Image:
    image = image.crop((0, 0, 320, 200))
    # image = ImageOps.scale(image, 0.3, resample=BICUBIC)
    return image


def row_2_picture(row: Tuple, with_data=True) -> Picture:
    if with_data:
        p = Picture(*row)
    else:
        p = Picture(row[0], None, *row[1:])
    p.created = datetime.datetime.fromtimestamp(p.created)
    return p


async def fetch_thumbnails_all_pictures(db, limit=100) -> List[Picture]:
    # uwaga: w systemie galerii powinien zwrócić obrazki _bez_ głównego pola "data"
    ans = []
    async with db.execute('SELECT pictureid, data_thumbnail, filename, description, creator_userid, created'
                          ' FROM pictures LIMIT ?', (limit,)) as cursor:
        async for row in cursor:
            # row to tuple typu (-1, b'001', b'0', 'a.jpg', 'something', 1, 1231234124.123)
            ans.append(row_2_picture(row, with_data=False))
    return ans


async def fetch_picture(db, pictureid) -> Picture:
    # pojedynczy obrazek, ale z wszystkimi danymi
    ans = []
    async with db.execute('SELECT * FROM pictures where pictureid=?', (pictureid,)) as cursor:
        async for row in cursor:
            ans.append(row_2_picture(row, with_data=True))
    return ans[0]


async def fetch_user(db, userid) -> User:
    # pojedynczy user
    ans = []
    async with db.execute('SELECT * FROM users where userid=?', (userid,)) as cursor:
        async for row in cursor:
            ans.append(User(*row))
    return ans[0]


async def fetch_users(db) -> List[User]:
    ans = []
    async with db.execute('SELECT * FROM users', ()) as cursor:
        async for row in cursor:
            ans.append(User(*row))
    return ans


async def file_2_picture(filename: str) -> Picture:
    image = Image.open(filename)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    bytes = image_bytes.getvalue()  # sposób na "wyrwanie" danych obrazka w postaci bytes (format PNG)

    thumb = await get_thumbnail(image)
    thumb_bytes = io.BytesIO()
    thumb.save(thumb_bytes, format='PNG')
    thb = thumb_bytes.getvalue()

    return Picture(-1, data=bytes, data_thumbnail=thb, filename=filename, description='',
                   creator_userid=-1, created=datetime.datetime.now())


async def pil_image_from_picture(picture: Picture, full_image=True) -> Image:
    if full_image:
        image = Image.open(io.BytesIO(picture.data))
    else:
        image = Image.open(io.BytesIO(picture.data_thumbnail))
    return image


async def db1():
    async with aiosqlite.connect('pic_db.db') as db:
        # await create_tables(db)
        # await delete_pictures(db)
        # user = await insert_user(db, User(-1, 'Kadabra1', 'xxx', '', True))
        # print(user)
        # print(await fetch_users(db))
        print(await fetch_thumbnails_all_pictures(db, 10))
        # pic: Picture = await file_2_picture('sample.png')
        # await insert_picture(db, pic)

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
