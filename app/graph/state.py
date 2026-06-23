from typing import TypedDict


class AgentState(TypedDict):

    query: str

    session_id: str

    memory_context: dict

    route: str

    plan: list

    memory_answer: str

    current_step: int

    step_results: list

    execution_trace: list

    tool_result: dict | None

    reflection: dict

    replan_count: int

    final_response: str
