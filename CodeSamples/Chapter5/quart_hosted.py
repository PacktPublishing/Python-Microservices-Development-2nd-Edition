# quart_basic.py
from quart import Quart

app = Quart(__name__)


@app.route("/api")
async def my_get_handler():
    return {"Hello": "World!"}


@app.route("/api_post", methods=["POST"])
async def my_post_handler():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="192.168.1.100")
