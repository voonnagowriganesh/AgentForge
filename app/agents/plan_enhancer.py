from app.core.logger import logger


class PlanEnhancer:

    def enhance(
        self,
        query: str,
        plan: list,
    ):

        enhanced_plan = []

        logger.info(
            "plan_enhancement_started",
            plan=plan,
        )

        for step in plan:

            enhanced_plan.append(step)

            #
            # document_search fallback
            #

            if step["tool"] == "document_search":

                enhanced_plan.append(
                    {
                        "step": len(enhanced_plan) + 1,
                        "tool": "web_search",
                        "input": query,
                    }
                )

                enhanced_plan.append(
                    {
                        "step": len(enhanced_plan) + 1,
                        "tool": "llm",
                        "input": query,
                    }
                )

                logger.info(
                    "document_fallback_added",
                    query=query,
                )

                return enhanced_plan

        logger.info(
            "plan_enhancement_completed",
            enhanced_plan=enhanced_plan,
        )

        return enhanced_plan


plan_enhancer = PlanEnhancer()
