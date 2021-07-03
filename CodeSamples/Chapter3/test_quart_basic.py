import json
import unittest

from quart_basic import app as app_under_test


class TestApp(unittest.IsolatedAsyncioTestCase):
    async def test_help(self):
        # creating a QuartClient instance to interact with the app
        app = app_under_test.test_client()

        # calling /api/ endpoint
        hello = await app.get("/api")

        # asserting the body
        body = json.loads(str(await hello.get_data(), "utf8"))
        self.assertEqual(body["Hello"], "World!")


if __name__ == "__main__":
    unittest.main()
