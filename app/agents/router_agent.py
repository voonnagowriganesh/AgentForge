from app.core.llm import llm

from app.prompts.router_prompt import ROUTER_PROMPT

from app.core.logger import logger

from app.core.retry import llm_retry


class RouterAgent:

    @llm_retry
    async def execute(self, query: str):
        logger.info("RouterAgent started", query=query)

        query_lower = query.lower().strip()

        if (
            query_lower.startswith("my name is")
            or query_lower.startswith("i live in")
            or query_lower.startswith("i work at")
            or query_lower.startswith("i am ")
            or query_lower.startswith("my favorite color is")
        ):
            logger.info(
                "router_short_circuit_memory_creation",
                query=query,
            )

            return "STORE"

        prompt = ROUTER_PROMPT.format(query=query)
        logger.info("router_prompt_prepared", prompt_length=len(prompt))

        result = await llm.invoke(prompt)
        route = result.strip().upper()

        logger.info("router_completed", route=route)
        return route


router_agent = RouterAgent()
