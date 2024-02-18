import asyncio

import aiohttp


class Binance:
    binance_api = 'https://api.binance.com/api/v3/'

    query_binnance = {
        'symbol': lambda pair: f'ticker/price?symbol={pair}',
        'symbols': lambda pairs: f'ticker/price?symbol={pairs}',
        'all': lambda pairs: 'ticker/price',
    }

    def prepare_data(self, response_courses):
        response_courses = response_courses if type(response_courses) == list else [response_courses]
        for course in response_courses:
            course['exchanger'] = 'binance'
            course['courses'] = {'direction': course.pop('symbol'), 'value': course.pop('price')}
        return response_courses[0] if len(response_courses) == 1 else response_courses

    async def get_courses(self, param, pairs):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(f'{self.binance_api}{self.query_binnance[param](pairs)}') as response:
                data = await response.json()
                return self.prepare_data(data)


class Coingecko:
    async def get_courses(self, pair):
        return ''


class StockMarket:

    def __init__(self):
        self.market_path = {
            'binance': 'https://api.binance.com/api/v3/ping',
            'coingecko': 'https://www.coingecko.com/api/ping'
        }
        self.stock_market = Binance()
        asyncio.create_task(self._check_path())

    async def _check_path(self):
        async with aiohttp.ClientSession(trust_env=True) as session:
            for market, path in self.market_path.items():
                response = await session.get(self.market_path['binance'])
                if response.status == 200:
                    if market == 'binance':
                        self.stock_market = Binance
                    else:
                        self.stock_market = Coingecko
                    break
                else:
                    raise Exception

    async def get_courses(self, param, pairs):
        return await self.stock_market.get_courses(param, pairs)
