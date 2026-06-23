import json

from app.core.llm import llm
from app.core.logger import logger


class ReflectionAgent:

    async def execute(
        self,
        query: str,
        step_results: list,
    ):

        logger.info(
            "reflection_started",
            query=query,
        )

        prompt = f"""
You are an AI Reflection Agent.

User Query:
{query}

Execution Results:
{step_results}

Determine whether these results are sufficient
to answer the user's query.

Return ONLY JSON.

Example:

{{
    "sufficient": true,
    "reason": "Enough information"
}}

OR

{{
    "sufficient": false,
    "reason": "Information missing",
    "next_tool": "web_search"
}}

Rules:

1. sufficient=true only if answer is complete.
2. If information is missing return sufficient=false.
3. next_tool can be:
   - web_search
   - document_search
   - memory
   - llm

Return only JSON.
"""

        response = await llm.invoke(prompt)

        logger.info(
            "reflection_completed",
            response=response,
        )

        try:

            return json.loads(response)

        except Exception as e:

            return {
                "sufficient": True,
                "reason": f"Failed to parse reflection {e}",
            }


reflection_agent = ReflectionAgent()
