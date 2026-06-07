from typing import TypedDict


class AgentState(TypedDict):

    query: str

    session_id: str

    memory_context: list

    route: str

    plan: list

    current_step: int

    step_results: list

    execution_trace: list

    tool_result: dict | None

    final_response: str
