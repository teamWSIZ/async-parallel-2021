import asyncio
from asyncio import sleep

from utils.naming import thread_name, task_name
from utils.profile import log


async def task(id):
    log(f'in task {id} {thread_name()}: {task_name()}')
    await sleep(0.5)


async def main():
    log('in main')
    await task(1)
    t1 = asyncio.create_task(task(0))
    await task(2)
    await sleep(1)

if __name__ == '__main__':
    log('start')
    log(thread_name())
    asyncio.run(main())
    log('done')