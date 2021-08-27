import asyncio

import aiohttp


async def make_request():
    urls = [
        "http://localhost:5000/api",
        "http://localhost:5000/api2",
    ]
    headers = {
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in urls:
            async with session.get(url) as response:
                print(await response.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
