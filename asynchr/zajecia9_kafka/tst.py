from asyncio import sleep
from unittest import IsolatedAsyncioTestCase


async def add(a, b):
    await sleep(0.01)
    return a + b


class Test(IsolatedAsyncioTestCase):

    async def test_functionality(self):
        result = await add(1, 2)
        self.assertEqual(3, result)
