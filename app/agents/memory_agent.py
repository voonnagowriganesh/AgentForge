from app.memory.store import (
    save_messages,
    get_messages,
    search_messages,
    get_memory_by_type,
)


from app.memory.store import delete_memory, upsert_user_memory
from app.utils.memory_utils import extract_forget_memory

from app.core.logger_tracing import trace_event

from app.core.logger import logger

from app.agents.memory_search_agent import memory_search_agent

import asyncio


class MemoryAgent:

    def retrieve_context(
        self,
        session_id: str,
    ):

        trace_event(f"{session_id}")

        return get_messages(session_id)

    def save_conversation(
        self,
        session_id: str,
        query: str,
        response: str,
    ):

        # metadata = {}

        # query_lower = query.lower().strip()

        # if query_lower.startswith("my name is"):
        #     metadata = {
        #         "memory_type": "name",
        #         "memory_value": query[11:].strip(),
        #     }

        # elif (
        #     query_lower.startswith("i live in")
        #     or "my current location is" in query_lower
        # ):
        #     metadata = {
        #         "memory_type": "location",
        #         "memory_value": query[9:].strip(),
        #     }

        metadata = {}

        query_lower = query.lower().strip()

        memory_to_delete = extract_forget_memory(query)

        if query.lower().startswith("forget") and memory_to_delete:

            delete_memory(
                session_id,
                memory_to_delete,
            )

        # Name
        if query_lower.startswith("my name is"):
            metadata = {
                "memory_type": "name",
                "memory_value": query[11:].strip(),
            }

        # Location
        elif query_lower.startswith("i live in"):
            metadata = {
                "memory_type": "location",
                "memory_value": query[9:].strip(),
            }

        # Company
        elif query_lower.startswith("i work at"):
            metadata = {
                "memory_type": "company",
                "memory_value": query[9:].strip(),
            }

        # Profession
        elif query_lower.startswith("i am an"):
            metadata = {
                "memory_type": "profession",
                "memory_value": query[7:].strip(),
            }

        elif query_lower.startswith("i am a"):
            metadata = {
                "memory_type": "profession",
                "memory_value": query[6:].strip(),
            }

        # Favorite Color
        elif query_lower.startswith("my favorite color is"):
            metadata = {
                "memory_type": "favorite_color",
                "memory_value": query[20:].strip(),
            }

        trace_event(f"Structured memory detected : {metadata}")

        trace_event(f"{session_id} , User query : {query}")

        if metadata.get("memory_type"):

            upsert_user_memory(
                session_id,
                metadata["memory_type"],
                metadata["memory_value"],
            )

            logger.info(
                "structured_memory_upsert_completed",
                session_id=session_id,
                memory_type=metadata["memory_type"],
            )

        

        save_messages(
            session_id,
            "user",
            query,
            metadata,
        )

        save_messages(
            session_id,
            "assistant",
            response,
        )

    async def search_context(self, session_id: str, query: str):

        memories = get_messages(session_id)

        relevant = await memory_search_agent.find_relevant_memories(
            query=query,
            memories=memories,
            session_id=session_id,
        )

        return relevant

    def get_structured_memory(
        self,
        session_id: str,
        memory_type: str,
    ):

        return get_memory_by_type(
            session_id,
            memory_type,
        )

    def get_all_structured_memories(
        self,
        session_id: str,
    ):
        memories = {}

        for memory_type in [
            "name",
            "location",
            "company",
            "profession",
            "favorite_color",
        ]:

            value = get_memory_by_type(
                session_id,
                memory_type,
            )

            if value:
                memories[memory_type] = value

        return memories


memory_agent = MemoryAgent()
