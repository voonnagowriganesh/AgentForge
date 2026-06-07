from app.memory.store import (
    save_messages,
    get_messages,
)

from app.core.logger_tracing import trace_event


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


memory_agent = MemoryAgent()
