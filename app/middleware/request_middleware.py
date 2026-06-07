import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger
from app.middleware.request_context import set_request_id


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        set_request_id(request_id)

        logger.info(
            "request_received",
            request_id=request_id,
            method=request.method,
            path=str(request.url),
        )

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        return response
