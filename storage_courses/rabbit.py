import json

import asyncio
import aio_pika
from tortoise import Tortoise

import settings
from redis import asyncio as aioredis
from storage_courses.models import Exchanger, Courses


async def upload_data_storage(message):
    redis = await aioredis.from_url(settings.REDIS_URL)
    courses = json.loads(message.body.decode())
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print(settings.ROOT_DIR)
    if type(courses) == dict:
        await redis.set(f'courses:symbol-{courses["courses"]["direction"]}', str(courses))
        exchanger = await Exchanger.get_or_create(exchanger=courses['exchanger'])
        courses_exists = await Courses.filter(direction=courses["courses"]['direction']).exists()
        if courses_exists is None:
            await Courses.create(direction=courses["courses"]['direction'], value=courses["courses"]['value'],
                                 exchanger=exchanger[0])
    else:
        pass


async def main() -> None:
    connection = await aio_pika.connect_robust(settings.RABBIT_MQ)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(settings.QUEUE_NAME, auto_delete=True)

        await queue.consume(upload_data_storage, no_ack=True)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
