import json

import asyncio
import uuid

import aio_pika
from tortoise import Tortoise

import settings
from redis import asyncio as aioredis
from models import Exchanger, Courses


async def upload_data_storage(message):
    redis = await aioredis.Redis(host=settings.REDIS_HOST, port=6379)
    courses_list = json.loads(message.body.decode())
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()
    for courses in courses_list:
        exchanger = await Exchanger.filter(exchanger=courses['exchanger'])
        if len(exchanger) == 0:
            exchanger = [await Exchanger.create(uid=uuid.uuid4(), exchanger=courses['exchanger'])]
        courses_exists = await Courses.filter(direction=courses["courses"]['direction']).exists()
        if not courses_exists:
            await Courses.create(uid=uuid.uuid4(), direction=courses["courses"]['direction'],
                                 value=courses["courses"]['value'], exchanger=exchanger[0])
        await redis.set(f'{settings.KEY_COURSES_REDIS}:{courses["courses"]["direction"]}', str(courses))


async def main() -> None:
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(settings.QUEUE_NAME, auto_delete=True)

        await queue.consume(upload_data_storage, no_ack=True)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
