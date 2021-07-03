# quart_logging.py
import logging
from quart import Quart, request

app = Quart(__name__)
app.logger.setLevel(logging.DEBUG)


@app.route("/hello")
def hello_handler():
    app.logger.info("hello_handler called")
    app.logger.debug(f"The request was {request}")
    return {"Hello": "World!"}


if __name__ == "__main__":
    app.run()
