import logging
import sys

import structlog

from app.core.config import get_settings
from app.middleware.request_context import get_request_id


def setup_logger():
    settings = get_settings()
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    return structlog.get_logger()


logger = setup_logger()


def log_event(event_name: str, **kwargs):
    logger.info(event_name, request_id=get_request_id(), **kwargs)


def console_log(message: str, **kwargs):
    logger.info("console_log", message=message, request_id=get_request_id(), **kwargs)
