from app.core.logger_tracing import console_log


async def search_web(query: str):

    console_log(f"Web search TOOL : {query}")

    return {
        "success": True,
        "tool": "web_search",
        "result": f"Search placeholder: {query}",
    }
