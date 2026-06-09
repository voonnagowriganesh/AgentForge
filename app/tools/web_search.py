from tavily import TavilyClient

from app.core.config import get_settings
from app.core.logger import logger

from app.schemas.tool_response import ToolResponse

from app.core.logger_tracing import console_log

from app.tools.search_summarizer import summarize_search_result

settings = get_settings()
client = TavilyClient(api_key=settings.TAVILY_API_KEY)


async def search_web(query: str):

    logger.info(
        "web_search_started",
        query=query,
    )

    response = client.search(query=query, max_results=3)

    results = []

    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
            }
        )

    logger.info(
        "web_search_completed",
        result_count=len(results),
    )

    summary = await summarize_search_result(
        query=query,
        results=results,
    )
    return ToolResponse(
        success=True,
        tool="web_search",
        result=summary,  # here for raw_result use response directly
    )
