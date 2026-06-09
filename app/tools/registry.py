from app.tools.calculator import calculate
from app.tools.datetime_tool import current_time
from app.tools.llm_tool import llm_tool
from app.tools.web_search import search_web

TOOLS = {
    "calculator": {
        "function": calculate,
        "description": "Math Calculations",
    },
    "datetime": {"function": current_time, "description": "Current time"},
    "llm": {
        "function": llm_tool,
        "description": "General reasoning",
    },
    "web_search": {
        "function": search_web,
        "description": "Search Current information from internet",
    },
}
