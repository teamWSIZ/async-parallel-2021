import asyncio
from asyncio import sleep

from utils.profile import log


async def job(n):
    log(f'starting job {n}')
    await sleep(1)
    log(f'ending job {n}')


async def add(a, b):
    await sleep(0.5)
    log('dodawanie skończone')
    return a + b


async def main():
    log('starting main')
    # await job(1)
    asyncio.create_task(job(1))
    asyncio.create_task(job(2))
    asyncio.create_task(job(3))
    asyncio.create_task(job(4))
    asyncio.create_task(job(5))

    suma = await add(5, 4)
    print(type(suma), suma)
    tX = asyncio.create_task(add(5, 5))
    print(type(tX), tX.done(), tX.cancelled())
    tX.cancel('some msg')
    await sleep(0)

    if not tX.cancelled():
        await tX
        print(type(tX), tX.done(), tX.cancelled())
        print(f'rezultat tX:{tX.result()}')


    # await job(2)
    log('finishing main')
    await sleep(2)
    log('koniec całości')


if __name__ == '__main__':
    asyncio.run(main())
