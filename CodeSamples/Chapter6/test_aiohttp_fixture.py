import asyncio
import aiohttp
import pytest
from aioresponses import aioresponses


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_ctx(mock_aioresponse):
    async with aiohttp.ClientSession() as session:
        mock_aioresponse.get("http://test.example.com", payload={"foo": "bar"})
        resp = await session.get("http://test.example.com")
        data = await resp.json()

    assert {"foo": "bar"} == data
