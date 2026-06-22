from app.core.logger import logger


class PlanValidator:

    def validate(
        self,
        query: str,
        plan: list,
        memory_context: dict = None,
    ):

        logger.info(
            "plan_validation_started",
            query=query,
            original_plan=plan,
        )

        validated_plan = []

        relevant_memory = []

        if memory_context:

            relevant_memory = memory_context.get(
                "relevant",
                [],
            )

        for step in plan:

            tool = step["tool"]

            #
            # Rule 1:
            # Memory should not answer general knowledge.
            #

            # if tool == "memory":

            #     if not relevant_memory:

            #         logger.info(
            #             "memory_tool_removed",
            #             reason="no_relevant_memory",
            #         )

            #         validated_plan.append(
            #             {
            #                 "step": 1,
            #                 "tool": "llm",
            #                 "input": query,
            #             }
            #         )

            if tool == "memory":

                query_lower = query.lower()

                GENERAL_KNOWLEDGE_PATTERNS = [
                    "capital",
                    "president",
                    "prime minister",
                    "ceo",
                    "founder",
                    "population",
                    "currency",
                ]

                #
                # Rule 1A:
                # Never use memory for general knowledge.
                #

                if any(
                    pattern in query_lower for pattern in GENERAL_KNOWLEDGE_PATTERNS
                ):

                    logger.info(
                        "memory_tool_replaced",
                        reason="general_knowledge_query",
                    )

                    validated_plan.extend(
                        [
                            {
                                "step": 1,
                                "tool": "web_search",
                                "input": query,
                            },
                            {
                                "step": 2,
                                "tool": "llm",
                                "input": query,
                            },
                        ]
                    )

                    break

                #
                # Rule 1B:
                # If no relevant memory exists,
                # fallback to llm.
                #

                if not relevant_memory:

                    logger.info(
                        "memory_tool_removed",
                        reason="no_relevant_memory",
                    )

                    validated_plan.append(
                        {
                            "step": 1,
                            "tool": "llm",
                            "input": query,
                        }
                    )

                    continue

            #
            # Rule 2:
            # document_search must always be followed by llm
            #

            validated_plan.append(step)

        if not validated_plan:

            validated_plan = [
                {
                    "step": 1,
                    "tool": "llm",
                    "input": query,
                }
            ]

        logger.info(
            "plan_validation_completed",
            validated_plan=validated_plan,
        )

        return validated_plan


plan_validator = PlanValidator()
