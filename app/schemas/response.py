from pydantic import BaseModel


class ChatResponse(BaseModel):
    response: str


class AgentResponse(BaseModel):

    query: str

    route: str

    final_response: str

    execution_trace: list
