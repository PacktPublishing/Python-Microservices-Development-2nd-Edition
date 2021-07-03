import logging

logger = logging.getLogger(__name__)


def default_outgoing(message, metadata):
    logger.warning("No outgoing message router for %s: %s", str(metadata), message)
