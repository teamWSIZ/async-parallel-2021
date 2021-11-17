import asyncio
from asyncio import sleep

async def add(a, b):
    await sleep(0.5)
    print('dodawanie skończone')
    return a + b


async def main():
    suma = await add(5, 4)
    await sleep(2)
    print('koniec')


if __name__ == '__main__':
    asyncio.run(main())
