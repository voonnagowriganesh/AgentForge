from app.schemas.tool_response import ToolResponse


def acknowledge_tool(message):

    return ToolResponse(
        success=True,
        tool="acknowledge",
        result=message,
    )
