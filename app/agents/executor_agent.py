from app.tools.registry import TOOLS

import inspect

from app.core.logger import logger

from app.core.exceptions import ToolNotFoundException

ALLOWED_TOOLS = {"calculator", "datetime", "llm", "web_search"}


class ExecutorAgent:

    async def execute(self, step: dict, memory_context=None):
        tool_name = step["tool"]
        tool_input = step["input"]

        logger.info(
            "executor_agent_start",
            tool=tool_name,
            tool_input=tool_input,
        )

        if tool_name not in ALLOWED_TOOLS:
            logger.error("unknown_tool", tool=tool_name)
            raise Exception(f"Unknown tool: {tool_name}")

        tool_meta = TOOLS.get(tool_name)

        tool = tool_meta["function"]

        if not tool:
            logger.error("tool_not_found", tool=tool_name)
            raise ToolNotFoundException(f"Tool {tool_name} not found")

        # if inspect.iscoroutinefunction(tool):
        #     result = await tool(tool_input)
        # else:
        #     result = tool(tool_input)

        if tool_name == "llm":

            result = await tool(tool_input, memory_context)

        elif inspect.iscoroutinefunction(tool):

            result = await tool(tool_input)

        else:

            result = tool(tool_input)

        logger.info(
            "executor_agent_completed",
            tool=tool_name,
            result_type=type(result).__name__,
            result_preview=str(result)[:200],
        )

        return result


executor_agent = ExecutorAgent()
