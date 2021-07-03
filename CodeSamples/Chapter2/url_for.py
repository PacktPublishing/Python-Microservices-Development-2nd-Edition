# Run url_for in an interactive Python environment.
# To start, run the python executable, and type the following as commands
# at the >>> prompt

from quart_converter import app
from quart import url_for
import asyncio


async def run_url_for():
    async with app.test_request_context("/", method="GET"):
        print(url_for("person", name="Tarek"))


loop = asyncio.get_event_loop()
loop.run_until_complete(run_url_for())
