from app.core.logger import logger
from app.middleware.request_context import get_request_id


def trace_event(event_name: str, **kwargs):
    """Log a structured event with the current request context."""
    logger.info(event_name, request_id=get_request_id(), **kwargs)


def console_log(message: str, **kwargs):
    """Emit a console-style log entry for business-level trace visibility."""
    logger.info("console_log", message=message, request_id=get_request_id(), **kwargs)
