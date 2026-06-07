from app.core.llm import llm
from app.core.logger import logger


async def llm_tool(query: str, memory_context=None):
    logger.info("llm_tool_started", query=query)

    prompt = f"""
    You are a helpful assistant.

    Conversation History:

    {memory_context}

    Answer the user using the conversation history when relevant.
    If it is not in conversation histroy answer directly

    Question:
    {query}
    """

    response = await llm.invoke(prompt)
    logger.info(
        "llm_tool_completed",
        response_length=len(response),
        response_preview=response[:200],
    )
    return {
        "success": True,
        "tool": "llm",
        "result": response,
    }
