import asyncio

import aiohttp


async def make_request():
    url = "http://192.168.1.100:8080/api"
    headers = {
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            print(await response.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
