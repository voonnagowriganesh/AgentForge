from app.memory.store import save_messages, get_messages, search_messages

from app.core.logger_tracing import trace_event

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

        trace_event(f"{session_id} , User query : {query}")

        save_messages(
            session_id,
            "user",
            query,
        )

        save_messages(
            session_id,
            "assistant",
            response,
        )

    async def search_context(self, session_id: str, query: str):

        memories = get_messages(session_id)

        relevant = await memory_search_agent.find_relevant_memories(
            query=query, memories=memories
        )

        return relevant


memory_agent = MemoryAgent()
