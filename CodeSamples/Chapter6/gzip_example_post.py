import asyncio
import gzip
import json

import aiohttp


async def make_request():
    url = "http://127.0.0.1:8080/api_post"
    headers = {
        "Content-Encoding": "gzip",
    }
    data = {"Hello": "World!", "result": "OK"}
    data = bytes(json.dumps(data), "utf8")
    data = gzip.compress(data)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as response:
            print(await response.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
