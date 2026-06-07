import re

from app.tools.registry import TOOLS

from app.core.logger import logger

from app.utils.math_parser import parse_math_query


import inspect


class ToolAgent:

    async def execute(self, query: str):
        query = query.lower()
        logger.info("ToolAgent started", query=query)

        if "time" in query:
            tool_meta = TOOLS["datetime"]
            tool = tool_meta["function"]
            logger.info("tool_selected", tool="datetime")
            if inspect.iscoroutinefunction(tool):
                return await tool("Current time")
            return tool("Current time")

        expression = parse_math_query(query)
        if expression:
            tool_meta = TOOLS["calculator"]
            tool = tool_meta["function"]

            logger.info(
                "tool_selected",
                tool="calculator",
                expression=expression,
                expression_type=type(expression).__name__,
            )

            if inspect.iscoroutinefunction(tool):
                return await tool(expression)

            return tool(expression)

        expression = re.sub(r"[^0-9+\-*/().]", "", query)
        if expression:
            tool_meta = TOOLS["calculator"]
            tool = tool_meta["function"]
            logger.info(
                "tool_selected",
                tool="calculator",
                expression=expression,
                expression_type=type(expression).__name__,
            )

            if inspect.iscoroutinefunction(tool):
                return await tool(expression)
            return tool(expression)

        logger.info("tool_agent_no_match", query=query)
        return "Tool not found"


tool_agent = ToolAgent()
