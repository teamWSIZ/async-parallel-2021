from asyncio import sleep
from random import randint
from unittest import IsolatedAsyncioTestCase

from faker import Faker

from asynchr.zajeciaz10_system_wiadomosci.auth_storage import AuthStorage


class Test(IsolatedAsyncioTestCase):
    db: AuthStorage

    # def setUp(self) -> None:
    #     pass
    #
    # def tearDown(self) -> None:
    #     pass

    async def asyncSetUp(self):
        print('before')
        self.db = AuthStorage('aa.db')
        await self.db.create_table_users()
        await self.db.create_table_topics()
        await self.db.cleanup_db()

    async def test_create_user_check_passwd(self):
        user = 'user'
        await self.db.insert_user(user, 'kadabra')
        res = await self.db.check_user(user, 'kadabra')
        self.assertEqual(res, True)

    async def test_create_user_wrong_passwd(self):
        user = 'user'
        await self.db.insert_user(user, 'kadabra')
        res = await self.db.check_user(user, 'bad-pass')
        self.assertEqual(res, False)


    async def test_create_multiple_users_with_same_name(self):
        user = 'user'
        await self.db.insert_user(user, 'kadabra')
        with self.assertRaises(Exception):
            await self.db.insert_user('ggg', 'kadabra')
        res = await self.db.check_user(user, 'bad-pass')
        self.assertEqual(res, False)


    async def test_update_passwd(self):
        user = 'user'
        await self.db.insert_user(user, 'kadabra')
        await self.db.update_password(user, 'kadabra', 'SECRET')
        res = await self.db.check_user(user, 'SECRET')
        self.assertEqual(res, True)

    async def test_update_oldpassword_does_not_work(self):
        user = 'user'
        await self.db.insert_user(user, 'kadabra')
        await self.db.update_password(user, 'kadabra', 'SECRET')
        res = await self.db.check_user(user, 'kadabra')
        self.assertEqual(res, False)

