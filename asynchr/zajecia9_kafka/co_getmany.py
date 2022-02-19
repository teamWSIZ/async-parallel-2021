import datetime

from aiokafka import AIOKafkaConsumer
import asyncio


async def consume():
    consumer = AIOKafkaConsumer('my_topic',
                                bootstrap_servers='10.10.35.1:9093',
                                group_id='ccc')
    # Get cluster layout and join group `my-group`
    await consumer.start()
    print('consumer started')
    try:
        # Consume messages
        messages = await consumer.getone()
        print(messages)
        # for msg in messages:
        #     print(msg.offset, msg.value, f'at {datetime.datetime.fromtimestamp(msg.timestamp//1000)}')
        # async for msg in consumer:
        #     print('consumed: ', msg.topic, msg.partition, msg.offset,
        #           msg.key, msg.value, msg.timestamp, f'at {datetime.datetime.fromtimestamp(msg.timestamp//1000)}')
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        print('consumer closed')


asyncio.run(consume())
