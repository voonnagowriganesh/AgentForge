from fastapi import FastAPI

from app.middleware.request_middleware import RequestMiddleware
from app.core.logger import logger
from app.core.exceptions import AgentException
from app.core.exception_handlers import agent_exception_handler

from app.api.routes import router

from app.db.database import init_db, migrate_db

app = FastAPI(title="AI Agent Platform")


init_db()
migrate_db()

logger.info("application_started", event_name="fastapi_app_initialized")

app.add_middleware(RequestMiddleware)
app.add_exception_handler(AgentException, agent_exception_handler)
app.include_router(router)


@app.get("/health")
async def health():
    logger.info("health_check", status="healthy")
    return {"status": "healthy"}
