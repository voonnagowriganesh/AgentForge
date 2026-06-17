from app.tools.registry import TOOLS

import inspect

from app.core.logger import logger

from app.memory.context_builder import build_memory_context

from app.rag.rag_tool import document_search

from app.core.exceptions import ToolNotFoundException

ALLOWED_TOOLS = {
    "calculator",
    "datetime",
    "llm",
    "web_search",
    "memory",
    "acknowledge",
    "profile",
    "document_search",
}


class ExecutorAgent:

    async def execute(
        self,
        step: dict,
        session_id: str,
        user_query,
        memory_context=None,
        previous_results=None,
    ):
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

        if tool_name == "memory":

            relevant_memory = memory_context.get("relevant", [])

            result = tool(relevant_memory)
        elif tool_name == "llm":

            logger.info(
                "llm_tool_debug",
                session_id=session_id,
                previous_results=previous_results,
            )

            memory_profile = build_memory_context(session_id)

            logger.info(
                "memory_context_injected",
                session_id=session_id,
                memory_context=memory_profile,
            )

            result = await tool(
                #tool_input,
                query = user_query,
                memory_context=memory_profile,
                previous_results=previous_results,
            )

        elif tool_name == "document_search":

            result = document_search(tool_input)

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
