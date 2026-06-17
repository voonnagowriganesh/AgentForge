from app.memory.store import get_memory_profile
from app.schemas.tool_response import ToolResponse
from app.core.logger import logger


def profile_tool(session_id):

    profile = get_memory_profile(session_id)

    logger.info(f"profile tool func executed with session id : {session_id}")

    profile_text = []

    for key, value in profile.items():

        if value:

            profile_text.append(f"{key}: {value}")

    return ToolResponse(
        success=True,
        tool="profile",
        result="\n".join(profile_text),
    )
