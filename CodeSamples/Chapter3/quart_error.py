# quart_basic.py
from quart import Quart

app = Quart(__name__)

text_404 = (
    "The requested URL was not found on the server.  "
    "If you entered the URL manually please check your "
    "spelling and try again."
)


@app.errorhandler(500)
def error_handling_500(error):
    return {"Error": str(error)}, 500


@app.errorhandler(404)
def error_handling_404(error):
    return {"Error": str(error), "description": text_404}, 404


@app.route("/api")
def my_microservice():
    raise TypeError("This is a testing exception.")


if __name__ == "__main__":
    app.run()
