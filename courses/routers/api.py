from typing import List, Dict

from fastapi import APIRouter, Query
from pydantic import BaseModel
from courses.stock_market import StockMarket
from courses.settings import REDIS_URL
from redis import asyncio as aioredis

router = APIRouter(
    tags=['API Exchanger']
)


class ExchangeCourses(BaseModel):
    exchanger: str
    courses: List[dict] | Dict


@router.get('/courses')
async def get_courses(symbol: str | None = None, symbols: List[str] = Query(None)):
    redis = await aioredis.from_url(REDIS_URL)
    stock_market = StockMarket()
    if symbol:
        key_symbol = f'courses:symbol-{symbol}'
        data_symbol = await redis.hgetall(key_symbol)
        if data_symbol:
            return ExchangeCourses(**data_symbol)
        else:
            course = await stock_market.get_courses('symbol', symbol)
            return ExchangeCourses(**course)
    else:
        pass
            # """
            # Отправить в Rabbit
            # сделать запрос по API вернуть данные
            # """
