import asyncio
import json
from dataclasses import dataclass

import aioredis
from aioredis import Redis


async def go(redis):
    await redis.set('my-key', 'value')
    val = await redis.get('my-key', encoding='utf-8')
    res = float(await redis.get('pi'))
    print(f'pi={res}')


async def get_users(redis, uids):
    # val = await redis.mget(' '.join(uids))
    val = await redis.mget(*uids)
    print(val)


@dataclass
class Car:
    vin: str
    price: int
    model: str


async def save_car(redis: Redis, c: Car):
    dane = json.dumps(c.__dict__)
    await redis.set(f'cars:{c.vin}', dane)

async def get_car_by_vin(redis: Redis, vin: str):
    key = f'cars:{vin}'
    dane = await redis.get(key)
    dane = dane.decode('utf-8')
    c = Car(**json.loads(dane))
    return c


async def main(loop):
    redis = await aioredis.create_redis_pool('redis://10.10.28.44', maxsize=4)
    print('connected')

    # for i in range(1):
    #     loop.create_task(go(redis))  # F&F
    # await asyncio.sleep(0.00)  # yield control
    # await get_users(redis, ['u1', 'u2', 'u1'])

    # await redis.set('pi', 3.14)
    # res = await redis.get('pi')
    #
    # await redis.sadd('s6000', 'car1')
    # await redis.sadd('s6000', 'car2')
    # await redis.sadd('s6000', 'car3')
    # await redis.sadd('s6000', 'car3')
    # await redis.sadd('s6000', 'car3')
    # vals = await redis.smembers('s6000')
    # print(vals)

    # zapis i odczyt instancji klas typu dataclass
    # c = Car('a11', 12, 'gg')
    # await save_car(redis, c)
    # c2 = await get_car_by_vin(redis,'a11')
    # print(c2)

    redis.zadd('gg', 10, 'gg10')
    redis.zadd('gg', 11, 'gg11')
    redis.zadd('gg', 12, 'gg12')
    redis.zadd('gg', 13, 'gg13')

    wybrane = await redis.zrangebyscore('gg', 11, 12)
    print(wybrane)


    print('shutting down')
    await asyncio.sleep(1)
    redis.close()
    await redis.wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
