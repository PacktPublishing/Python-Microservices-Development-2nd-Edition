# quart_profiled.py
import flask_profiler
import quart.flask_patch  # noqa
from quart import Quart

app = Quart(__name__)

app.config["DEBUG"] = True

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {"engine": "sqlite"},
    "basicAuth": {"enabled": True, "username": "admin", "password": "admin"},
    "ignore": ["^/static/.*"],
}


@app.route("/api")
def my_microservice():
    return {"Hello": "World!"}


flask_profiler.init_app(app)


if __name__ == "__main__":
    app.run()
