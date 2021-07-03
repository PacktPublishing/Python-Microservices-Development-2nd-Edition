# hypercorn_server.py
from quart import Quart

app = Quart(__name__)


@app.route("/api")
def my_microservice():
    return {"Hello": "World!"}
