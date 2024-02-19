import asyncio
import aiohttp
from redis import asyncio as aioredis

import settings
from settings import COINGECKO_API_KEY


class Binance:
    binance_api = 'https://data-api.binance.vision/api/v3/'

    query_binnance = {
        'symbol': lambda pair: f'ticker/price?symbol={pair.replace("-", "")}',
        'symbols': lambda pairs: "ticker/price?symbols=" + str(pairs).replace("\'", "\"").
                                                            replace('-', '').replace(" ", ""),
        'all': lambda pairs: 'ticker/price',
    }

    def prepare_data(self, response_courses, pairs):
        response_courses = response_courses if type(response_courses) == list else [response_courses]
        pairs = {pair.replace("-", ''): pair for pair in pairs}
        for course in response_courses:
            course['exchanger'] = 'binance'
            course['courses'] = {'direction': pairs[course.pop('symbol')], 'value': course.pop('price')}
        return response_courses[0] if len(response_courses) == 1 else response_courses

    async def get_courses(self, param, pairs):
        pairs = pairs if type(pairs) == list else [pairs]
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(f'{self.binance_api}{self.query_binnance[param](pairs)}') as response:
                data = await response.json()
                return self.prepare_data(data, pairs)


class Coingecko:
    coingecko_api = 'https://api.coingecko.com/api/v3/'

    async def search_ids(self, symbol):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                    f'{self.coingecko_api}/search?query={symbol}&x_cg_demo_api_key={COINGECKO_API_KEY}') as response:
                data = await response.json()
                for coin in data['coins']:
                    if coin['symbol'] == symbol:
                        return coin['id']

    def prepare_data(self, response_courses, ids, pair):
        return {
            'exchanger': 'coingecko',
            'courses': {
                'direction': pair,
                'value': response_courses[ids][pair.split("-")[1].lower()]
            }
        }

    async def get_courses(self, param, pairs):
        redis = await aioredis.from_url(settings.REDIS_URL)
        if param == 'symbol':
            data_symbol = await redis.get(f'{settings.KEY_COURSES_REDIS}:{pairs}')
            if data_symbol:
                return data_symbol.decode()
            ids = await self.search_ids(pairs.split('-')[0])
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                        f'{self.coingecko_api}/simple/price?ids={ids}&vs_currencies={pairs.split("-")[1]}') as response:
                    data = await response.json()
                    return self.prepare_data(data, ids, pairs)
        else:
            arr_courses = []
            for pair in pairs:
                data_symbol = await redis.get(f'{settings.KEY_COURSES_REDIS}:{pairs}')
                if data_symbol:
                    arr_courses.append(data_symbol.decode())
                ids = await self.search_ids(pair.split('-')[0])
                async with aiohttp.ClientSession(trust_env=True) as session:
                    response = await session.get(
                        f'{self.coingecko_api}/simple/price?ids={ids}&vs_currencies={pair.split("-")[1]}')
                    data = await response.json()
                    arr_courses.append(self.prepare_data(data, ids, pair))
            return arr_courses


class StockMarket:

    def __init__(self):
        self.market_path = {
            'binance': 'https://data-api.binance.vision/api/v3/ping',
            'coingecko': f'https://api.coingecko.com/api/v3/ping?x_cg_demo_api_key={COINGECKO_API_KEY}'
        }
        self.stock_market = Binance()
        asyncio.create_task(self._check_path())

    async def _check_path(self):
        async with aiohttp.ClientSession(trust_env=True) as session:
            for market, path in self.market_path.items():
                response = await session.get(self.market_path['binance'])
                if response.status == 200:
                    self.stock_market = Coingecko()
                    break
                else:
                    raise Exception

    async def get_courses(self, param, pairs):
        await self._check_path()
        return await self.stock_market.get_courses(param, pairs)
