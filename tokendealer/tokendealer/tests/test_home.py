import os
import pytest

os.environ["TESTDIR"] = os.path.dirname(__file__)

from tokendealer.app import app as quart_app  # NOQA

_SECRET = "f0fdeb1f1584fd5431c4250b2e859457"


@pytest.fixture
def app():
    return quart_app


@pytest.mark.asyncio
async def test_get_pub_key(app):
    client = app.test_client()
    response = await client.get("/.well-known/jwks.json")
    assert response.status_code == 200
    json_data = await response.json
    assert "n" in json_data[0]


@pytest.mark.asyncio
async def test_roundtrip(app):
    client = app.test_client()
    data = {
        "client_id": "worker1",
        "client_secret": _SECRET,
        "audience": "audience",
        "grant_type": "client_credentials",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await client.post("/oauth/token", form=data, headers=headers)
    data = await response.json
    data["audience"] = "audience"

    response = await client.post("/verify_token", form=data)
    json_response = await response.json
    assert json_response["iss"] == "https://tokendealer.example.com"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token,expected", (({"access_token": "d.A.D"}, 400), ({}, 400))
)
async def test_bad_tokens(app, token, expected):
    client = app.test_client()
    response = await client.post("/verify_token", json=token)
    assert response.status_code == expected
