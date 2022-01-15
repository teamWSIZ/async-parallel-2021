import asyncio
from asyncio import sleep

import aiohttp


async def upload():
    # client upload to url
    session = aiohttp.ClientSession()
    files = {'file': open('bio1.jpg', 'rb')}
    print('have file')
    async with await session.post('http://localhost:4001/upload', data=files) as resp:
        if resp.status == 200:
            print(f'upload complete; result: {await resp.json()}')
    await sleep(0.1)
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(upload())

