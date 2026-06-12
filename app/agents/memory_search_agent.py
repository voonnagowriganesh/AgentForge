from app.core.llm import llm
from app.core.logger import logger
from app.memory.store import (
    get_memory_by_type,
    delete_user_memory,
    get_user_memory,
    get_all_user_memories,
)
from app.memory.store import get_all_memories, search_similar_memories

from app.memory.embedding_service import embedding_service


import json


class MemorySearchAgent:

    async def find_relevant_memories(
        self,
        query: str,
        memories: list,
        session_id: str,
    ):

        query_lower = query.lower().strip()

        if (
            query_lower.startswith("my name is")
            or query_lower.startswith("i live in")
            or query_lower.startswith("i work at")
            or query_lower.startswith("i am ")
            or query_lower.startswith("my favorite color is")
        ):
            logger.info(
                "memory_creation_query_detected",
                query=query,
            )

            return []

        logger.info("memory_debug", memories=memories)

        if not memories:
            logger.info(
                "no_recent_memory_found",
                session_id=session_id,
            )
            return []

        logger.info(
            "query_check",
            query=query,
            query_lower=query_lower,
        )

        if "forget my location" in query_lower:

            delete_user_memory(
                session_id,
                "location",
            )

            logger.info(
                "forget_memory_executed",
                memory_type="location",
            )

            return ["Location memory removed successfully."]
        # Name

        if any(
            phrase in query_lower
            for phrase in [
                "my name",
                "what is my name",
                "who am i",
            ]
        ):

            logger.info(
                "structured_memory_lookup",
                memory_type="name",
                session_id=session_id,
            )

            name = get_user_memory(
                session_id,
                "name",
            )

            if name:
                logger.info(
                    "structured_memory_found",
                    memory_type="name",
                    value=name,
                )

                return [name]

            logger.info(
                "structured_memory_not_found",
                memory_type="name",
            )

            return ["NO_NAME_FOUND"]

        if any(
            phrase in query_lower
            for phrase in [
                "where do i live",
                "my location",
                "where am i from",
            ]
        ):

            logger.info(
                "structured_memory_lookup",
                memory_type="location",
                session_id=session_id,
            )

            location = get_user_memory(
                session_id,
                "location",
            )

            if location:
                logger.info(
                    "structured_memory_found",
                    memory_type="location",
                    value=location,
                )
                return [location]

            logger.info(
                "structured_memory_not_found",
                memory_type="location",
            )

            return ["NO_LOCATION_FOUND"]

        if any(
            phrase in query_lower
            for phrase in [
                "where do i work",
                "my company",
                "which company",
            ]
        ):
            logger.info(
                "structured_memory_lookup",
                memory_type="company",
                session_id=session_id,
            )

            company = get_user_memory(
                session_id,
                "company",
            )

            if company:
                logger.info(
                    "structured_memory_found",
                    memory_type="company",
                    value=company,
                )
                return [company]

            return ["NO_COMPANY_FOUND"]

        if any(
            phrase in query_lower
            for phrase in [
                "my profession",
                "what do i do",
                "my job",
            ]
        ):

            logger.info(
                "structured_memory_lookup",
                memory_type="profession",
                session_id=session_id,
            )

            profession = get_user_memory(
                session_id,
                "profession",
            )

            if profession:
                logger.info(
                    "structured_memory_found",
                    memory_type="profession",
                    value=profession,
                )
                return [profession]

            logger.info(
                "structured_memory_not_found",
                memory_type="profession",
            )

            return ["NO_PROFESSION_FOUND"]

        if any(
            phrase in query_lower
            for phrase in [
                "favorite color",
                "favourite color",
            ]
        ):

            logger.info(
                "structured_memory_lookup",
                memory_type="favorite_color",
                session_id=session_id,
            )

            color = get_user_memory(
                session_id,
                "favorite_color",
            )

            if color:
                logger.info(
                    "structured_memory_found",
                    memory_type="color",
                    value=color,
                )
                return [color]

            logger.info(
                "structured_memory_not_found",
                memory_type="color",
            )

            return ["NO_COLOR_FOUND"]

        if any(
            phrase in query_lower
            for phrase in [
                "what do you know about me",
                "tell me about me",
                "my profile",
            ]
        ):

            logger.info(
                "profile_summary_requested",
                session_id=session_id,
            )

            return get_all_user_memories(
                session_id
            )  # need to replace this with actual session_id

        #         prompt = f"""
        # You are a memory retrieval agent.

        # Current User Query:
        # {query}

        # Conversation History:
        # {memories}

        # Instructions:

        # - Select memories that help answer the current query.
        # - Match semantically, not only exact words.
        # - Resolve references such as he, she, it, they, this, that, his, her.
        # - If the query asks for a person's name, retrieve memories containing that name.
        # - If wording differs but the memory contains the answer, return it.
        # - Prefer returning potentially useful memories rather than returning nothing.
        # - Exclude clearly unrelated memories.

        # Return ONLY valid JSON array of memory contents.

        # Example:

        # [
        #   "My name is John"
        # ]
        # """

        #         result = await llm.invoke(prompt)

        #         logger.info(
        #             "memory_search_agent_completed",
        #             result_preview=result[:200],
        #         )

        #         try:
        #             return json.loads(result)

        #         except Exception as e:
        #             logger.error(f"Error enocuntred in MemorySearchAgent class {e}")

        query_embedding = embedding_service.generate_embedding(query)

        logger.info(
            "query_embedding_generated",
            query=query,
        )

        results = search_similar_memories(
            session_id=session_id,
            query_embedding=query_embedding,
            top_k=5,
        )

        if not results:

            logger.info(
                "no_semantic_memory_found",
                query=query,
                session_id=session_id,
            )

        logger.info(
            "semantic_search_results",
            results_preview=str(results)[:300],
        )

        logger.info(
            "semantic_search_completed",
            count=len(results),
        )

        return results


memory_search_agent = MemorySearchAgent()
