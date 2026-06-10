from app.schemas.tool_response import ToolResponse
from app.core.logger import logger


def memory_tool(memory_data):

    if not memory_data:
        result = ""

    elif isinstance(memory_data, list):
        result = memory_data[0]

    else:
        result = str(memory_data)

    return ToolResponse(success=True, tool="memory", result=result)
