# quart_cors.py
from quart import Quart
from quart_cors import cors, route_cors

app = Quart(__name__)
app = cors(app, allow_origin="https://quart.com")
# app = cors(app, allow_origin="*")


@app.route("/api")
# @route_cors(allow_origin=["https://quart.com"])
async def my_microservice():
    return {"Hello": "World!"}


if __name__ == "__main__":
    # app.config["QUART_CORS_ALLOW_ORIGIN"] = ["http://quart.com"]
    # app = cors(app, allow_origin=["http://befuddle.flummox.org:5200"])
    print(app.config)
    app.run(port=5200)
