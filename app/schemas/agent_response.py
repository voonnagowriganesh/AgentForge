from pydantic import BaseModel


class AgentResponse(BaseModel):

    success: bool

    response: str

    request_id: str

    trace: list

