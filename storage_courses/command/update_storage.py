import asyncio
from redis import asyncio as aioredis
import time

import settings
from storage_courses.models import Courses
from utils.stock_market import Binance, Coingecko
from tortoise import Tortoise
from settings import TORTOISE_ORM


async def update_storage(course):
    redis = await aioredis.from_url(settings.REDIS_URL)
    if course.exchanger.exchanger == 'binance':
        market = Binance()
    else:
        market = Coingecko()
    data = await market.get_courses('symbol', course.direction)
    await redis.set(f'{settings.KEY_COURSES_REDIS}:{data["courses"]["direction"]}', str(data))
    course.value = data['courses']['value']
    await course.save()


async def main():
    while True:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

        all_courses = await Courses.all().select_related('exchanger')
        await asyncio.gather(*[update_storage(course) for course in all_courses])
        time.sleep(3)


asyncio.run(main())
