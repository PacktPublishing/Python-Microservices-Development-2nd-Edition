# logging_example.py

import logging

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

logger.info("This is an informational message")

data = {"a": 1}
logger.debug("The data I am processing is %s" % data)
