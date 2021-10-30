import asyncio
import concurrent.futures
import math
import time
from asyncio import sleep, current_task

from utils.profile import log, tn, task_name


def heavy_operation():
    """
    Model ciężkiej operacji... nieprzygotowanej do async.
    """
    log('heavey operation')
    # log(f'heavy running in task: {task_name()}')

    log(f'heavy operation on thead {tn()}:')
    time.sleep(10)  # blocking; not async
    log('heavy operation - END')
    return math.pi ** 100


async def small_ops():
    log(f'Starting small ops on thread {tn()}')
    log(f'small running in task: {task_name()}')

    while True:
        print('.', end='')
        await sleep(0.25)


async def main():
    asyncio.create_task(small_ops())
    log(f'main running in task: {task_name()}')
    await sleep(2)

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, heavy_operation)
    log(result)

    await sleep(100)


if __name__ == '__main__':
    log(f'Startujemy program na wątku: {tn()}')
    asyncio.run(main())
