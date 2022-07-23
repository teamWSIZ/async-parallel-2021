import datetime
from aiokafka import AIOKafkaConsumer
import asyncio

async def consume():
    consumer = AIOKafkaConsumer('my_topic1', 'my_other_topic',
                                bootstrap_servers='10.10.35.1:9093',
                                group_id='ggg2')
    await consumer.start()
    print('consumer started')
    try:
        async for msg in consumer:
            print('consumed: ', msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp, f'at {datetime.datetime.fromtimestamp(msg.timestamp//1000)}')
    finally:
        await consumer.stop()


asyncio.run(consume())
