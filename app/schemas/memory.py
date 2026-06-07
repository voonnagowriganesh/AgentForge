from pydantic import BaseModel


class MemoryRecord(BaseModel):

    session_id: str

    role: str

    content: str
