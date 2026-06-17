from app.tools.calculator import calculate
from app.tools.datetime_tool import current_time
from app.tools.llm_tool import llm_tool
from app.tools.web_search import search_web
from app.tools.memory_tool import memory_tool
from app.tools.profile_tool import profile_tool
from app.tools.acknowledge_tool import acknowledge_tool
from app.rag.rag_tool import document_search

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
    "memory": {
        "description": "Retrieve answer directly from meomory",
        "function": memory_tool,
    },
    "acknowledge": {
        "function": acknowledge_tool,
        "description": "Generate storage acknowledgement",
    },
    "profile": {
        "function": profile_tool,
        "description": "Retrieve user profile",
    },
    "document_search":{
        "function":document_search,
        "description":"Search uploaded document"
    }
}
