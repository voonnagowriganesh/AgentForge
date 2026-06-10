from app.core.llm import llm
from app.core.logger import logger

import json


class MemorySearchAgent:

    async def find_relevant_memories(
        self,
        query: str,
        memories: list,
    ):

        logger.info("memory_debug", memories=memories)

        if not memories:
            return []

        query_lower = query.lower()

        logger.info(
            "query_check",
            query=query,
            query_lower=query_lower,
        )

        if any(
            phrase in query_lower
            for phrase in ["my name", "what is my name", "who am i"]
        ):

            logger.info("name_branch_triggered")
            for msg in memories:

                if (
                    msg.get("role") == "user"
                    and "my name is" in msg.get("content", "").lower()
                ):
                    return [msg["content"]]
            return ["NO_NAME_FOUND"]

        prompt = f"""
You are a memory retrieval agent.

Current User Query:
{query}

Conversation History:
{memories}

Instructions:

- Select memories that help answer the current query.
- Match semantically, not only exact words.
- Resolve references such as he, she, it, they, this, that, his, her.
- If the query asks for a person's name, retrieve memories containing that name.
- If wording differs but the memory contains the answer, return it.
- Prefer returning potentially useful memories rather than returning nothing.
- Exclude clearly unrelated memories.

Return ONLY valid JSON array of memory contents.

Example:

[
  "My name is John"
]
"""

        result = await llm.invoke(prompt)

        logger.info(
            "memory_search_agent_completed",
            result_preview=result[:200],
        )

        try:
            return json.loads(result)

        except Exception as e:
            logger.error(f"Error enocuntred in MemorySearchAgent class {e}")


memory_search_agent = MemorySearchAgent()
