from app.schemas.tool_response import ToolResponse
from app.core.logger import logger


def memory_tool(memory_data):

    if isinstance(memory_data, dict):

        profile = []

        for key, value in memory_data.items():
            profile.append(f"{key.replace('_',' ').title()}: {value}")

        result = "\n".join(profile)

    elif not memory_data:

        result = ""

    elif isinstance(memory_data, list):

        result = ""

        for item in memory_data:

            if isinstance(item, tuple):

                score, role, content = item

                content_lower = content.lower()

                if (
                    content.endswith("?")
                    or "the question is" in content_lower
                    or "not explicitly stated" in content_lower
                    or "tool result" in content_lower
                    or "confidence score" in content_lower
                ):
                    continue

                result = content
                break

            else:

                result = item
                break

        logger.info(
            "memory_tool_selected_result",
            result_preview=str(result)[:100],
        )

    else:

        result = str(memory_data)

    return ToolResponse(
        success=True,
        tool="memory",
        result=result,
    )
