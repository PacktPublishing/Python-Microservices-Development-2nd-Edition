import asyncio
import aiohttp
import pytest
from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_ctx():
    with aioresponses() as mocked:
        async with aiohttp.ClientSession() as session:
            mocked.get("http://test.example.com", payload={"foo": "bar"})
            resp = await session.get("http://test.example.com")
            data = await resp.json()

        assert {"foo": "bar"} == data
