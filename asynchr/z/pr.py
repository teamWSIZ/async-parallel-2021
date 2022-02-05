import datetime

from aiokafka import AIOKafkaProducer
import asyncio

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='10.10.35.1:9093', enable_idempotence=True)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        gg = await producer.send_and_wait('my_topic', b'Super message 1')
        print(f'done at {datetime.datetime.now()}')
        print(gg)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())