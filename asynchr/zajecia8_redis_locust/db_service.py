import asyncio
import json
from asyncio import sleep
from dataclasses import asdict
from typing import List

from aioredis import Redis
import aioredis

from asynchr.zajecia8_redis_locust.model import HKRunner, get_time_from_str

REDIS = 'redis://10.10.28.44'
KEY = 'HK1'  # key for results (ZSET)


class DbService:
    redis: Redis

    async def initialize(self):
        self.redis = await aioredis.create_redis_pool(REDIS, maxsize=20)

    async def close(self):
        await self.redis.shutdown()  # todo: check this

    async def save_runners_result(self, result: HKRunner):
        data = json.dumps(asdict(result))
        score = result.time
        await self.redis.zadd(KEY, score, data)

    async def get_results_for_times(self, mintime: int, maxtime: int) -> List[HKRunner]:
        res = await self.redis.zrangebyscore(KEY, mintime, maxtime)
        result = []
        # print(res)  #[b'{"race_no": 101010, "country": "Portugal", "time": 11111}', b'{"race_no": 101011, "country": "Algieria", "time": 11112}']
        for bs in res:
            data = json.loads(bs.decode('UTF-8'))
            hkr = HKRunner(**data)
            result.append(hkr)
            # print(hkr)
        return result


async def mm():
    srv = DbService()
    await srv.initialize()
    # await srv.save_runners_result(HKRunner(101011, 'Algieria', 11112))
    # await srv.save_runners_result(HKRunner(2, 'Ethiopia', 130))
    rr = await srv.get_results_for_times(11000, 12000)
    print(rr)


if __name__ == '__main__':
    asyncio.run(mm())
