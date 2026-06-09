from app.core.llm import llm
from app.core.logger import logger

# async def summarize_search_result(query: str, results: list):

#     logger.info(
#         "search_summarizer_started",
#         query=query,
#         results_count=len(results),
#     )

#     context = ""

#     for idx, item in enumerate(results, start=1):

#         title = item.get("title", "")
#         content = item.get("content", "")

#         context += f"""
#         Result {idx}

#         Title:
#         {title}

#         content:
#         {content}"""

#         prompt = f"""
#         You are a research assistant.

#         Using the search results below,
#         answer the user's query.

#         User Query:
#         {query}

#         Search Results:

#         {context}

#         Rules:

#         - Give a concise answer.
#         - Use bullet points if appropriate.
#         - Do not mention search result numbers.
#         - Do not invent information."""

#         summary = await llm.invoke(prompt)

#         logger.info(
#             "search_summarizer_completed",
#             summary_preview=summary[:200],
#         )

#     return summary


async def summarize_search_result(query: str, results: list):

    logger.info(
        "search_summarizer_started",
        query=query,
        results_count=len(results),
    )

    context = ""

    for idx, item in enumerate(results, start=1):

        title = item.get("title", "")
        content = item.get("content", "")

        context += f"""
Result {idx}

Title:
{title}

Content:
{content}

"""

    prompt = f"""
You are a research assistant.

Using the search results below,
answer the user's query.

User Query:
{query}

Search Results:

{context}

Rules:

- Give a concise answer.
- Use bullet points if appropriate.
- Do not mention search result numbers.
- Do not invent information.
"""

    summary = await llm.invoke(prompt)

    logger.info(
        "search_summarizer_completed",
        summary_preview=summary[:200],
    )

    return summary
