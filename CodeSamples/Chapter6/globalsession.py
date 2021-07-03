import asyncio

import aiohttp
from quart import Quart, g as quart_globals


async def get_connector():
    if "clientsession" not in quart_globals:
        headers = {"Content-Type": "application/json"}
        quart_globals.clientsession = aiohttp.ClientSession(headers=headers)
    return quart_globals.clientsession


app = Quart(__name__)


@app.route("/api")
async def my_microservice():
    conn = await get_connector()
    # conn = aiohttp.ClientSession()
    async with conn.get("http://localhost:5000/api") as response:
        sub_result = await response.json()
    return {"result": sub_result, "Hello": "World!"}


if __name__ == "__main__":
    app.run(port=5001)
