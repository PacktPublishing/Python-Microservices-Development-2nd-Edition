# quart_structlog.py
import logging
from quart import Quart, request
import structlog
from structlog import wrap_logger
from structlog.processors import JSONRenderer

app = Quart(__name__)

logger = wrap_logger(
    app.logger,
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(),
        JSONRenderer(indent=4, sort_keys=True),
    ],
)
app.logger.setLevel(logging.DEBUG)


@app.route("/hello")
def hello_handler():
    logger.info("hello_handler called")
    logger.debug(f"The request was {request}")
    return {"Hello": "World!"}


if __name__ == "__main__":
    app.run()
