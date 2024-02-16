import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool


import asyncio
import logging

import aio_pika

import settings


async def main() -> None:
    connection = await aio_pika.connect_robust(settings.RABBIT_MQ)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(settings.QUEUE_NAME, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message)


if __name__ == "__main__":
    asyncio.run(main())