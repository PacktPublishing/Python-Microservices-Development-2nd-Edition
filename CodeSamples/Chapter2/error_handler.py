# error_handler.py
from quart import Quart

app = Quart(__name__)


@app.errorhandler(500)
def error_handling(error):
    return {"Error": str(error)}, 500


@app.route("/api")
def my_microservice():
    raise TypeError("Some Exception")


if __name__ == "__main__":
    app.run()
