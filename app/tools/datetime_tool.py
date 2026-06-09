from datetime import datetime

from app.schemas.tool_response import ToolResponse


def current_time(time):

    result = datetime.now().isoformat()

    return ToolResponse(
        success=True,
        tool="datetime",
        result=result,
    ).model_dump()
