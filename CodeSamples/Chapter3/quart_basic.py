# quart_basic.py
from quart import Quart

app = Quart(__name__)


@app.route("/api")
def my_microservice():
    return {"Hello": "World!"}


if __name__ == "__main__":
    app.run()
