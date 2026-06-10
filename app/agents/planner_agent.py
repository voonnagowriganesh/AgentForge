from app.core.llm import llm
from app.core.logger import logger

from app.prompts.planner_prompt import PLANNER_PROMPT

from app.core.retry import llm_retry

from app.schemas.plan import Plan
from app.tools.helper import get_available_tools


class PlannerAgent:

    @llm_retry
    async def execute(
        self,
        query: str,
        memory: list,
    ):
        logger.info("PlannerAgent started", query=query)

        tools = get_available_tools()
        prompt = PLANNER_PROMPT.format(
            query=query,
            tools=tools,
            recent_memory=memory["recent"],
            relevant_memory=memory["relevant"],
        )
        logger.info("planner_prompt_prepared", prompt_length=len(prompt))

        query_lower = query.lower().strip()

        if query_lower.startswith("my name is"):

            name = query[11:].strip()

            return {
                "plan": [
                    {
                        "step": 1,
                        "tool": "acknowledge",
                        "input": f"Name stored successfully: {name}",
                    }
                ]
            }

        if query_lower.startswith("i live in"):

            location = query[9:].strip()

            return {
                "plan": [
                    {
                        "step": 1,
                        "tool": "acknowledge",
                        "input": f"Location stored successfully: {location}",
                    }
                ]
            }
        result = await llm.invoke(prompt)
        result = result.strip()
        logger.info("planner_raw_response", response_preview=result[:250])

        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        try:
            parsed_plan = Plan.model_validate_json(result)
            plan_payload = parsed_plan.model_dump()

            logger.info("planner_completed", plan=plan_payload)
            return plan_payload

        except Exception as e:
            logger.info(f"Planner Agent Exception encountred {e}")

            return {"plan": [{"step": 1, "tool": "llm", "input": query}]}


planner_agent = PlannerAgent()
