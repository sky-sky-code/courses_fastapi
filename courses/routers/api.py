import asyncio
import json
from typing import List, Dict

from fastapi import APIRouter, Query
from pydantic import BaseModel

from utils.stock_market import StockMarket
import settings
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


async def get_data_and_publish(stock_market, symbol):
    data_symbol = await stock_market.get_courses('symbol', symbol)
    print(data_symbol)
    asyncio.create_task(publisher(json.dumps([data_symbol])))
    return ExchangeCourses(**data_symbol)


@router.get('/courses')
async def get_courses(symbols: List[str] = Query(None)):
    redis = await aioredis.from_url(settings.REDIS_URL)
    stock_market = StockMarket()
    courses_list = []
    index, len_symbols = 0, len(symbols)
    while index < len_symbols:
        data_symbol = await redis.get(f'{settings.KEY_COURSES_REDIS}:{symbols[index]}')
        if data_symbol:
            courses_list.append(ExchangeCourses(**json.loads(data_symbol.decode().replace('\'', '\"'))))
            symbols.pop(index)
            index, len_symbols = index - 1, len(symbols)
        index += 1
    data = await asyncio.gather(*[get_data_and_publish(stock_market, not_found_symbol) for not_found_symbol in symbols])
    return courses_list + data
