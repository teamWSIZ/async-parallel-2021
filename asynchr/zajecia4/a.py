import asyncio
import concurrent.futures


def blocking_io():
    with open('/dev/urandom', 'rb') as f:
        return f.read(1000000)


def cpu_bound(msg1, msg2):
    print(msg1)
    print(msg2)
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound, 'aa', 'bb')
        print('custom process pool', result)


asyncio.run(main())
