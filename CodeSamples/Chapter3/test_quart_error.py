# test_quart_error.py
import json
import unittest

from quart_error import app as app_under_test
from quart_error import text_404


class TestApp(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a client to interact with the app
        self.app = app_under_test.test_client()

    async def test_raise(self):
        # This won't raise a Python exception but return a 500
        hello = await self.app.get("/api")
        self.assertEqual(hello.status_code, 500)

    async def test_proper_404(self):
        # Call a non-existing endpoint
        hello = await self.app.get("/dwdwqqwdwqd")

        # It's not there
        self.assertEqual(hello.status_code, 404)

        # but we still get a nice JSON body
        body = json.loads(str(await hello.get_data(), "utf8"))
        self.assertEqual(hello.status_code, 404)
        self.assertEqual(
            body["Error"],
            "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        )
        self.assertEqual(body["description"], text_404)


if __name__ == "__main__":
    unittest.main()
