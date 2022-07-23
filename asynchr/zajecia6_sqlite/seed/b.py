import asyncio

from utils.naming import task_name


async def f1():
    print(task_name())
    await f2()

async def f2():
    print(task_name())



if __name__ == '__main__':
    asyncio.run(f1())
