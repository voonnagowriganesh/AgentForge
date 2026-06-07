from app.agents.tool_agent import tool_agent
from app.agents.planner_agent import planner_agent


AGENTS = {
    "TOOL":tool_agent,
    "PLAN":planner_agent
}
