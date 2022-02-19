import asyncio
import datetime
from asyncio import sleep
from dataclasses import dataclass
from random import randint

import aiohttp_cors
from aiohttp import web
from aiokafka import AIOKafkaConsumer

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


message_storage = dict()    # username -> List[KafkaMessage]


@dataclass
class KafkaMessage:
    offset: int
    topic: int
    value: str


async def consumer_job(username, storage):
    consumer = AIOKafkaConsumer('my_topic',
                                bootstrap_servers='10.10.35.1:9093',
                                group_id='ggx2')
    # Get cluster layout and join group `my-group`
    await consumer.start()
    print('consumer started')
    try:
        # Consume messages
        async for msg in consumer:
            # print('consumed: ', msg.topic, msg.partition, msg.offset,
            #       msg.key, msg.value, msg.timestamp, f'at {datetime.datetime.fromtimestamp(msg.timestamp // 1000)}')
            k_message = KafkaMessage(msg.offset, msg.topic, msg.value.decode('utf-8'))
            print(f'consumed: {k_message}')
            storage[username].append(k_message)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


@routes.get('/getmessages')
async def getmsg(request):
    username = request.rel_url.query['name']
    if username not in message_storage:
        message_storage[username] = []
        asyncio.create_task(consumer_job(username, message_storage))
        await sleep(1)
    res = [m.__dict__ for m in message_storage[username]]
    message_storage[username] = []

    return web.json_response({'messages': res})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=4001)
