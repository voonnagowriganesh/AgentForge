from fastapi.responses import JSONResponse

from app.core.logger import logger


async def agent_exception_handler(request, exc):
    logger.error(
        "agent_exception", error=str(exc), path=str(request.url), method=request.method
    )
    return JSONResponse(status_code=400, content={"success": False, "error": str(exc)})
