import asyncio

import aiosqlite


class AuthStorage:
    filename: str

    def __init__(self, filename):
        self.filename = filename

    async def create_table_users(self):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('create table if not exists users (username text unique, password text)')
            await db.commit()

    async def create_table_topics(self):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('create table if not exists topics (topic text unique, secret text)')
            await db.commit()

    async def cleanup_db(self):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('delete from users where true')
            await db.execute('delete from topics where true')
            await db.commit()

    async def insert_user(self, name, password):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('insert into users(username, password) values(?, ?)', (name, password))
            await db.commit()

    async def check_user(self, username, password) -> bool:
        async with aiosqlite.connect(self.filename) as db:
            async with await db.execute('select * from users where username = ? and password = ?',
                                        (username, password)) as cursor:
                u = await cursor.fetchone()
                if u:
                    return True
                else:
                    return False

    async def update_password(self, username, old_password, new_password):
        if not await self.check_user(username, old_password):
            raise Exception('Wrong password')
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('update users set password=? where username=?', (new_password, username))
            await db.commit()



    async def insert_topic(self, topic, secret):
        async with aiosqlite.connect(self.filename) as db:
            await db.execute('insert into topics(topic, secret) values(?, ?)', (topic, secret))
            await db.commit()

    async def check_topic(self, topic, secret) -> bool:
        async with aiosqlite.connect(self.filename) as db:
            async with await db.execute('select * FROM topics where topic = ? adn secret = ?',
                                        (topic, secret)) as cursor:
                t = await cursor.fetchone()
                if t:
                    return True
                else:
                    return False


if __name__ == '__main__':
    async def main():
        db = AuthStorage('aa.db')
        await db.create_table_users()
        await db.insert_user('abra', 'kadabra')

    asyncio.run(main())