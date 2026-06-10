from app.core.llm import llm
from app.core.logger import logger
from app.schemas.tool_response import ToolResponse


async def llm_tool(query: str, memory_context=None, previous_results=None):
    logger.info("llm_tool_started", query=query)

    if previous_results:

        prompt = f"""
        You are an AI assistant.

        Tool Results:
        {previous_results}

        Task:
        {query}

        Use ONLY the tool results to answer.

        Answer:
        """

    else:

        prompt = f"""
        You are an AI assistant.

        User Question:
        {query}

        Memory:
        {memory_context}

        Use memory if relevant.

        Answer:
        """

    #     prompt = f"""
    # You are an AI assistant.

    # Task:
    # {query}

    # Tool Results:
    # {previous_results}

    # Memory:
    # {memory_context}

    # Rules:

    # 1. If Tool Results are available, use Tool Results as the primary source.
    # 2. Memory is secondary.
    # 3. Answer the task directly.
    # 4. Never ignore Tool Results.
    # 5. Do not say "not found" if Tool Results contain the answer.

    # Answer:
    # """

    print("Previous result", previous_results)

    response = await llm.invoke(prompt)
    logger.info(
        "llm_tool_completed",
        response_length=len(response),
        response_preview=response[:200],
    )
    return ToolResponse(
        success=True,
        tool="llm",
        result=response,
    ).model_dump()
