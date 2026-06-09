from pydantic import BaseModel

from app.core.logger import logger


class AgentResponse(BaseModel):

    logger.info("AgentResponse class Executing")

    success: bool

    response: str

    request_id: str

    trace: list
