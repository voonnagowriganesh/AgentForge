from pydantic import BaseModel

from app.core.logger import logger


class ChatResponse(BaseModel):
    response: str


class AgentResponse(BaseModel):

    logger.info("AgentResponse class Executing")

    query: str

    route: str

    final_response: str

    execution_trace: list
