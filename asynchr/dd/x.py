import asyncio
from asyncio.subprocess import PIPE


async def foo():
    process = await asyncio.create_subprocess_shell(f'ls -lah', stdin=PIPE, stdout=PIPE, stderr=PIPE)

    # await process finish
    (stdout, stderr) = await process.communicate()
    if stdout.__contains__(b'error') or stdout.__contains__(b'warning'):
        raise Exception(f'error: {stdout}')
    if stderr.__len__() > 0:
        raise Exception(f'error: {stderr}')
    # print(stdout)   #bytes
    stdout_s = stdout.decode()
    print(stdout_s)
    print('ls done')


if __name__ == '__main__':
    asyncio.run(foo())
