from typing import Any

from app.core.logger import logger

from pydantic import BaseModel


class ToolResponse(BaseModel):

    logger.info("Tool Response class Executing")

    success: bool

    tool: str

    result: Any
