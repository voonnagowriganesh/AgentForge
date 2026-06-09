from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.agents.router_agent import router_agent

from app.agents.planner_agent import planner_agent

from app.agents.executor_agent import executor_agent

from app.agents.tool_agent import tool_agent

from app.agents.memory_agent import memory_agent

from app.utils.result_parser import extract_result

from app.core.logger import logger

# async def planner_node(state):
#     plan = await planner_agent.execute(state["query"])

#     return {"plan": plan["plan"], "current_step": 0}


async def planner_node(state):

    plan = await planner_agent.execute(state["query"], state["memory_context"])
    trace = state.get("execution_trace", [])
    trace.append({"agent": "planner", "steps": plan["plan"]})

    logger.info("planner_node_completed", query=state["query"], plan=plan)
    return {"plan": plan["plan"], "current_step": 0, "execution_trace": trace}


# async def router_node(state):

#     route = await router_agent.execute(state["query"])

#     return {"route": route}


async def router_node(state):

    route = await router_agent.execute(state["query"])
    trace = state.get("execution_trace", [])
    trace.append({"agent": "router", "output": route})

    logger.info("router_node_completed", query=state["query"], route=route)
    return {"route": route, "execution_trace": trace}


def route_decision(state):

    if state["route"] == "TOOL":
        logger.info("route_decision", route=state["route"], next_node="tool")
        return "tool"

    logger.info("route_decision", route=state["route"], next_node="planner")
    return "planner"


async def tool_node(state):
    result = await tool_agent.execute(state["query"])
    logger.info(
        "tool_node_completed", query=state["query"], tool_result=str(result)[:200]
    )
    return {"tool_result": result}


async def executor_node(state):

    idx = state["current_step"]

    task = state["plan"][idx]

    result = await executor_agent.execute(task, state["memory_context"])

    trace = state.get("execution_trace", [])

    results = state.get("step_results", [])

    results.append(result)

    trace.append(
        {"agent": "executor", "tool": task["tool"], "output": extract_result(result)}
    )

    logger.info(
        "executor_step_completed",
        step=idx,
        tool=task["tool"],
        result_preview=str(result)[:200],
    )

    return {"step_results": results, "current_step": idx + 1, "execution_trace": trace}


async def memory_node(state):

    memory = memory_agent.retrieve_context(state["session_id"])

    logger.info("Memory_node Completed ", memory=memory)

    return {"memory_context": memory}


async def response_node(state):
    if state.get("tool_result"):
        final_response = extract_result(state["tool_result"])
        logger.info("response_node_completed", final_response=final_response)
        return {"final_response": final_response}

    # final_response = "\n".join(state["step_results"])

    # last_result = state["step_results"][-1]

    # if isinstance(last_result, dict):

    #     final_response = str(last_result.get("result", last_result))

    # else:

    #     final_response = str(last_result)

    final_response = "\n".join(extract_result(x) for x in state["step_results"])

    memory_agent.save_conversation(
        session_id=state["session_id"],
        query=state["query"],
        response=final_response,
    )

    logger.info("response_node_completed", final_response=final_response)

    return {"final_response": final_response}


def continue_execution(state):

    if state["current_step"] < len(state["plan"]):
        return "executor"

    return "end"


builder = StateGraph(AgentState)

builder.add_node("router", router_node)

builder.add_node("tool", tool_node)

builder.add_node("planner", planner_node)


builder.add_node("executor", executor_node)

builder.add_node("memory", memory_node)


builder.add_node("response", response_node)

builder.set_entry_point("memory")

builder.add_edge("memory", "router")

builder.add_conditional_edges(
    "router", route_decision, {"tool": "tool", "planner": "planner"}
)

builder.add_edge("tool", "response")

builder.add_edge("planner", "executor")

builder.add_conditional_edges(
    "executor", continue_execution, {"executor": "executor", "end": "response"}
)

builder.add_edge("response", END)

graph = builder.compile()
