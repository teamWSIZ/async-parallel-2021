import asyncio
import concurrent.futures
import time
from asyncio import sleep

from utils.profile import log, tn


def heavy_operation():
    log('heavey operation')
    print('heavy:', tn())
    time.sleep(5)  # blocking; not async
    log('heavy operation - END')


async def small_ops():
    print('small', tn())
    while True:
        print('.', end='')
        await sleep(0.25)


async def main():
    asyncio.create_task(small_ops())

    await sleep(1)

    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, heavy_operation)
    await sleep(100)


if __name__ == '__main__':
    asyncio.run(main())
