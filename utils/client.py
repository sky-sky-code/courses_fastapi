#!/usr/bin/env python

import asyncio
import json

import websockets

req = """
{    
"method": "SUBSCRIBE",
"params":
[
"btcusdt@aggTrade",
"btcusdt@depth"
],
"id": 1
}
"""

dct = {"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"], "id": 1}


async def main():
    uri = "wss://fstream.binance.com/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(dct))

        data = await websocket.recv()
        print(websocket.messages)


if __name__ == '__main__':
    asyncio.run(main())
