import asyncio
from asyncio import sleep

from utils.profile import log


async def job(n):
    log(f'starting job {n}')
    await sleep(1)
    log(f'ending job {n}')


async def main():
    log('starting main')
    # await job(1)
    asyncio.create_task(job(1))
    log('-----')
    asyncio.create_task(job(2))
    # await job(2)
    log('finishing main')
    await sleep(2)


if __name__ == '__main__':
    asyncio.run(main())