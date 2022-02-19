from asyncio import sleep
from unittest import IsolatedAsyncioTestCase


async def add(a, b):
    await sleep(0.01)
    return a + b


class Test(IsolatedAsyncioTestCase):

    async def test_simple_add(self):
        result = await add(1, 2)
        self.assertEqual(3, result)

    async def test_huge_add(self):
        result = await add(10**30, 10**30)
        self.assertEqual(2 * 10**30, result)
