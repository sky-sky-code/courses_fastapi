import asyncio
import json
from typing import List, Dict

from fastapi import APIRouter, Query
from pydantic import BaseModel

import settings
from utils.stock_market import StockMarket
from redis import asyncio as aioredis
import aio_pika

router = APIRouter(
    tags=['API Exchanger']
)


class ExchangeCourses(BaseModel):
    exchanger: str
    courses: List[dict] | Dict


async def publisher(message):
    connection = await aio_pika.connect_robust(settings.RABBIT_MQ)
    async with connection:
        routing_key = settings.QUEUE_NAME

        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=routing_key,
        )


@router.get('/courses')
async def get_courses(symbol: str | None = None, symbols: List[str] = Query(None)):
    if symbols is not None and len(symbols) == 1:
        symbol = symbols[0]
    redis = await aioredis.from_url(settings.REDIS_URL)
    stock_market = StockMarket()
    if symbol:
        data_symbol = await redis.get(f'{settings.KEY_COURSES_REDIS}:{symbol}')
        if data_symbol:
            return ExchangeCourses(**json.loads(data_symbol.decode().replace('\'', '\"')))
        else:
            course = await stock_market.get_courses('symbol', symbol)
            asyncio.create_task(publisher(json.dumps([course])))
            return ExchangeCourses(**course)
    elif symbols:
        courses_list = await stock_market.get_courses('symbols', symbols)
        asyncio.create_task(publisher(json.dumps(courses_list)))
        return [ExchangeCourses(**courses) for courses in courses_list]