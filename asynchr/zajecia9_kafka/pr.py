import datetime
from asyncio import sleep

from aiokafka import AIOKafkaProducer
import asyncio

from faker import Faker

from utils.profile import ts


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='10.10.35.1:9093')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    fake = Faker()
    try:
        # Produce message
        while True:
            n = fake.name()
            dst = fake.address()
            msg = f'{n} on his way to {dst}'
            gg = await producer.send_and_wait('my_topic', msg.encode())
            print(f'message sent at {datetime.datetime.now()}')
            await sleep(1)
        # print(gg)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())