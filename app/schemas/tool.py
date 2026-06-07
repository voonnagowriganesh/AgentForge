from pydantic import BaseModel


class ToolResult(BaseModel):

    success: bool

    tool: str

    result: str | int | float | dict | list
