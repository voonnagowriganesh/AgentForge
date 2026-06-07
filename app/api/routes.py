from fastapi import APIRouter

from app.core.logger import logger
from app.core.logger_tracing import console_log
from app.graph.workflow import graph
from app.schemas.request import ChatRequest
from app.schemas.response import AgentResponse

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    console_log(f"Received chat request: {request.query}")
    logger.info("chat_request_received", query=request.query)

    result = await graph.ainvoke(
        {
            "query": request.query,
            "session_id": request.session_id,
            "memory_context": [],
            "step_results": [],
            "execution_trace": [],
        }
    )

    logger.info(
        "chat_request_completed",
        query=request.query,
        route=result.get("route"),
        response_length=len(str(result.get("final_response", ""))),
    )

    return AgentResponse(
        query=result["query"],
        route=result["route"],
        final_response=result["final_response"],
        execution_trace=result["execution_trace"],
    )
